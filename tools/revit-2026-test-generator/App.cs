using System.Diagnostics;
using System.Reflection;
using System.Security.Cryptography;
using System.Text.Json;
using Autodesk.Revit.ApplicationServices;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Architecture;
using Autodesk.Revit.DB.Structure;
using Autodesk.Revit.UI;
using Autodesk.Revit.UI.Events;

namespace Eem.Revit2026TestGenerator;

[Transaction(TransactionMode.Manual)]
public sealed class App : IExternalApplication
{
    private const string EnabledVariable = "EEM_REVIT_TEST_GENERATOR";
    private const string OutputVariable = "EEM_REVIT_TEST_OUTPUT";
    private const string TemplateVariable = "EEM_REVIT_TEST_TEMPLATE";
    private bool _started;

    public Result OnStartup(UIControlledApplication application)
    {
        if (!string.Equals(Environment.GetEnvironmentVariable(EnabledVariable), "1", StringComparison.Ordinal))
        {
            return Result.Succeeded;
        }

        application.Idling += OnIdling;
        return Result.Succeeded;
    }

    public Result OnShutdown(UIControlledApplication application) => Result.Succeeded;

    private void OnIdling(object? sender, IdlingEventArgs args)
    {
        if (_started || sender is not UIApplication uiApplication)
        {
            return;
        }

        _started = true;
        uiApplication.Idling -= OnIdling;

        string outputRoot = Environment.GetEnvironmentVariable(OutputVariable)
            ?? throw new InvalidOperationException($"Falta la variable {OutputVariable}.");
        string templatePath = Environment.GetEnvironmentVariable(TemplateVariable)
            ?? throw new InvalidOperationException($"Falta la variable {TemplateVariable}.");

        Directory.CreateDirectory(outputRoot);
        string logPath = Path.Combine(outputRoot, "revit-generator.log");

        try
        {
            Log(logPath, "Inicio del generador Revit 2026.");
            Log(logPath, $"Plantilla: {templatePath}");

            Document document = uiApplication.Application.NewProjectDocument(templatePath);
            BuildModel(document, logPath);

            string rvtPath = Path.Combine(outputRoot, "eem-revit-2026-modelo-minimo.rvt");
            document.SaveAs(rvtPath, new SaveAsOptions { OverwriteExistingFile = true });
            Log(logPath, $"RVT guardado: {rvtPath}");

            List<ExportRecord> exports = ExportMatrix(document, outputRoot, logPath);
            WriteManifest(uiApplication.Application, outputRoot, rvtPath, exports);
            Log(logPath, "Ensayo generado correctamente.");

            File.WriteAllText(
                Path.Combine(outputRoot, "DONE"),
                DateTimeOffset.Now.ToString("O"));
        }
        catch (Exception exception)
        {
            Log(logPath, exception.ToString());
            File.WriteAllText(Path.Combine(outputRoot, "FAILED"), exception.ToString());
        }
        finally
        {
            try
            {
                RevitCommandId exitCommand = RevitCommandId.LookupPostableCommandId(PostableCommand.ExitRevit);
                if (uiApplication.CanPostCommand(exitCommand))
                {
                    uiApplication.PostCommand(exitCommand);
                }
            }
            catch (Exception exception)
            {
                Log(logPath, $"No se pudo solicitar el cierre de Revit: {exception.Message}");
            }
        }
    }

    private static void BuildModel(Document document, string logPath)
    {
        using Transaction transaction = new(document, "Crear modelo mínimo energético");
        transaction.Start();

        ProjectInfo project = document.ProjectInformation;
        SetText(project.get_Parameter(BuiltInParameter.PROJECT_NAME), "EEM Revit 2026 Modelo Minimo");
        SetText(project.get_Parameter(BuiltInParameter.PROJECT_BUILDING_NAME), "EEM_EDIFICIO_ENSAYO");
        SetText(project.get_Parameter(BuiltInParameter.PROJECT_NUMBER), "EEM-R26-001");

        AreaVolumeSettings.GetAreaVolumeSettings(document).ComputeVolumes = true;

        List<Level> levels = new FilteredElementCollector(document)
            .OfClass(typeof(Level))
            .Cast<Level>()
            .OrderBy(level => level.Elevation)
            .ToList();

        Level baseLevel = levels.First();
        Level upperLevel = levels.FirstOrDefault(level => level.Elevation > baseLevel.Elevation + ToFeet(2.5))
            ?? Level.Create(document, baseLevel.Elevation + ToFeet(3.0));
        baseLevel.Name = "EEM_N00";
        upperLevel.Name = "EEM_N01_CUBIERTA";

        WallType exteriorType = FirstBasicWallType(document);
        WallType partitionType = DuplicateWallTypeIfRequired(exteriorType, "EEM_PARTICION_INTERIOR");
        exteriorType.Function = WallFunction.Exterior;
        partitionType.Function = WallFunction.Interior;
        FloorType sourceFloorType = new FilteredElementCollector(document)
            .OfClass(typeof(FloorType))
            .Cast<FloorType>()
            .First(type => !type.IsFoundationSlab);
        FloorType floorType = DuplicateFloorTypeIfRequired(sourceFloorType, "EEM_SUELO_EXTERIOR");
        FloorType roofType = DuplicateFloorTypeIfRequired(sourceFloorType, "EEM_CUBIERTA_PLANA");
        SetInteger(floorType.get_Parameter(BuiltInParameter.FUNCTION_PARAM), 1);
        SetInteger(roofType.get_Parameter(BuiltInParameter.FUNCTION_PARAM), 1);

        double width = ToFeet(12.0);
        double depth = ToFeet(8.0);
        double height = upperLevel.Elevation - baseLevel.Elevation;

        XYZ p00 = new(0, 0, baseLevel.Elevation);
        XYZ p10 = new(width, 0, baseLevel.Elevation);
        XYZ p11 = new(width, depth, baseLevel.Elevation);
        XYZ p01 = new(0, depth, baseLevel.Elevation);

        Wall southWall = CreateWall(document, p00, p10, exteriorType, baseLevel, height);
        CreateWall(document, p10, p11, exteriorType, baseLevel, height);
        CreateWall(document, p11, p01, exteriorType, baseLevel, height);
        CreateWall(document, p01, p00, exteriorType, baseLevel, height);
        Wall partition = CreateWall(
            document,
            new XYZ(width / 2, 0, baseLevel.Elevation),
            new XYZ(width / 2, depth, baseLevel.Elevation),
            partitionType,
            baseLevel,
            height);

        CurveLoop floorBoundary = RectangleLoop(p00, p10, p11, p01);
        Floor.Create(document, new List<CurveLoop> { floorBoundary }, floorType.Id, baseLevel.Id);

        CurveLoop roofBoundary = RectangleLoop(
            new XYZ(0, 0, upperLevel.Elevation),
            new XYZ(width, 0, upperLevel.Elevation),
            new XYZ(width, depth, upperLevel.Elevation),
            new XYZ(0, depth, upperLevel.Elevation));
        Floor roof = Floor.Create(document, new List<CurveLoop> { roofBoundary }, roofType.Id, upperLevel.Id);
        roof.Name = "EEM_CUBIERTA_PLANA";

        document.Regenerate();
        PlaceHostedFamily(
            document,
            @"C:\ProgramData\Autodesk\RVT 2026\Libraries\Spanish\Puertas\Puerta-Hueco.rfa",
            new XYZ(width / 2, depth / 2, baseLevel.Elevation),
            partition,
            baseLevel);
        PlaceHostedFamily(
            document,
            @"C:\ProgramData\Autodesk\RVT 2026\Libraries\Spanish\Ventanas\Ventana batiente 1.rfa",
            new XYZ(width / 4, 0, baseLevel.Elevation + ToFeet(1.2)),
            southWall,
            baseLevel);

        FamilyInstance? column = PlaceFreeFamily(
            document,
            @"C:\ProgramData\Autodesk\RVT 2026\Libraries\Spanish\Pilares\Pilar rectangular.rfa",
            new XYZ(width / 4, depth / 2, baseLevel.Elevation),
            baseLevel);
        if (column is not null)
        {
            Parameter? roomBounding = column.get_Parameter(BuiltInParameter.WALL_ATTR_ROOM_BOUNDING);
            if (roomBounding is { IsReadOnly: false })
            {
                roomBounding.Set(0);
            }
        }

        document.Regenerate();
        Room leftRoom = document.Create.NewRoom(baseLevel, new UV(width / 4, depth / 2));
        leftRoom.Name = "EEM_ZONA_OESTE";
        leftRoom.Number = "EEM-01";
        SetUpperLimit(leftRoom, upperLevel);

        Room rightRoom = document.Create.NewRoom(baseLevel, new UV(width * 0.75, depth / 2));
        rightRoom.Name = "EEM_ZONA_ESTE";
        rightRoom.Number = "EEM-02";
        SetUpperLimit(rightRoom, upperLevel);

        ViewFamilyType view3dType = new FilteredElementCollector(document)
            .OfClass(typeof(ViewFamilyType))
            .Cast<ViewFamilyType>()
            .First(type => type.ViewFamily == ViewFamily.ThreeDimensional);
        View3D view = View3D.CreateIsometric(document, view3dType.Id);
        view.Name = "EEM_IFC_EXPORT_ALL";

        document.Regenerate();
        transaction.Commit();

        Log(logPath, $"Modelo creado con habitaciones {leftRoom.Number} y {rightRoom.Number}.");
    }

    private static List<ExportRecord> ExportMatrix(Document document, string outputRoot, string logPath)
    {
        string ifcDirectory = Path.Combine(outputRoot, "ifc");
        Directory.CreateDirectory(ifcDirectory);

        (string Name, IFCVersion Version, int BoundaryLevel)[] matrix =
        {
            ("eem-r26-ifc2x3-cv2-sb0", IFCVersion.IFC2x3CV2, 0),
            ("eem-r26-ifc2x3-cv2-sb1", IFCVersion.IFC2x3CV2, 1),
            ("eem-r26-ifc2x3-cv2-sb2", IFCVersion.IFC2x3CV2, 2),
            ("eem-r26-ifc4-rv-sb0", IFCVersion.IFC4RV, 0),
            ("eem-r26-ifc4-rv-sb1", IFCVersion.IFC4RV, 1),
            ("eem-r26-ifc4-rv-sb2", IFCVersion.IFC4RV, 2),
            ("eem-r26-ifc4-dtv-sb2", IFCVersion.IFC4DTV, 2)
        };

        List<ExportRecord> records = new();
        foreach ((string name, IFCVersion version, int boundaryLevel) in matrix)
        {
            IFCExportOptions options = new()
            {
                FileVersion = version,
                SpaceBoundaryLevel = boundaryLevel,
                ExportBaseQuantities = true,
                WallAndColumnSplitting = true
            };
            ApplyIfcUiConfiguration(document, options, version, boundaryLevel);
            options.AddOption("ExportIFCCommonPropertySets", "true");
            options.AddOption("ExportInternalRevitPropertySets", "true");
            options.AddOption("ExportSchedulesAsPsets", "false");
            options.AddOption("Use2DRoomBoundaryForVolume", "false");
            options.AddOption("StoreIFCGUID", "false");

            bool status;
            string? error = null;
            Transaction exportTransaction = new(document, $"Exportar {name}");
            try
            {
                exportTransaction.Start();
                status = document.Export(ifcDirectory, name, options);
            }
            catch (Exception exception)
            {
                status = false;
                error = exception.ToString();
            }
            finally
            {
                if (exportTransaction.GetStatus() == TransactionStatus.Started)
                {
                    exportTransaction.RollBack();
                }
            }

            string path = Path.Combine(ifcDirectory, name + ".ifc");
            records.Add(new ExportRecord(
                name,
                version.ToString(),
                boundaryLevel,
                status,
                File.Exists(path) ? path : null,
                File.Exists(path) ? Sha256(path) : null,
                error));
            Log(logPath, $"Exportación {name}: {(status ? "OK" : "FALLO")}");
        }

        return records;
    }

    private static void ApplyIfcUiConfiguration(
        Document document,
        IFCExportOptions options,
        IFCVersion version,
        int boundaryLevel)
    {
        Assembly assembly = AppDomain.CurrentDomain.GetAssemblies()
            .FirstOrDefault(item => item.GetName().Name == "Autodesk.IFC.Export.UI")
            ?? Assembly.LoadFrom(
                @"C:\Program Files\Autodesk\Revit 2026\AddIns\IFCExporterUI\Autodesk.IFC.Export.UI.dll");
        Type commandType = assembly.GetType("BIM.IFC.Export.UI.IFCCommandOverrideApplication", true)!;
        PropertyInfo? documentProperty = commandType.GetProperty(
            "TheDocument",
            BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static);
        FieldInfo? documentField = commandType.GetField(
            "TheDocument",
            BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static);
        if (documentProperty is not null)
        {
            documentProperty.SetValue(null, document);
        }
        else if (documentField is not null)
        {
            documentField.SetValue(null, document);
        }
        else
        {
            throw new InvalidOperationException("No se pudo asignar el documento a la interfaz IFC de Revit.");
        }

        Type configurationType = assembly.GetType("BIM.IFC.Export.UI.IFCExportConfiguration", true)!;
        object configuration = Activator.CreateInstance(configurationType)!;
        SetConfiguration(configurationType, configuration, "IFCVersion", version);
        SetConfiguration(configurationType, configuration, "SpaceBoundaries", boundaryLevel);
        SetConfiguration(configurationType, configuration, "SplitWallsAndColumns", true);
        SetConfiguration(configurationType, configuration, "ExportBaseQuantities", true);
        SetConfiguration(configurationType, configuration, "ExportIFCCommonPropertySets", true);
        SetConfiguration(configurationType, configuration, "ExportInternalRevitPropertySets", true);
        configurationType.GetMethod("UpdateOptions")!.Invoke(
            configuration,
            new object[] { options, ElementId.InvalidElementId });
    }

    private static void SetConfiguration(
        Type configurationType,
        object configuration,
        string propertyName,
        object value) =>
        configurationType.GetProperty(propertyName)!.SetValue(configuration, value);

    private static void WriteManifest(
        Application application,
        string outputRoot,
        string rvtPath,
        List<ExportRecord> exports)
    {
        string exporterPath = Path.Combine(
            Path.GetDirectoryName(Process.GetCurrentProcess().MainModule?.FileName) ?? string.Empty,
            "Revit.IFC.Export.dll");
        string? exporterVersion = File.Exists(exporterPath)
            ? FileVersionInfo.GetVersionInfo(exporterPath).FileVersion
            : null;

        object manifest = new
        {
            generated_at = DateTimeOffset.Now.ToString("O"),
            revit = new
            {
                version_name = application.VersionName,
                version_number = application.VersionNumber,
                version_build = application.VersionBuild,
                subversion = application.SubVersionNumber
            },
            ifc_exporter = new
            {
                path = exporterPath,
                version = exporterVersion
            },
            model = new
            {
                path = rvtPath,
                sha256 = Sha256(rvtPath)
            },
            exports
        };

        File.WriteAllText(
            Path.Combine(outputRoot, "manifest.json"),
            JsonSerializer.Serialize(manifest, new JsonSerializerOptions { WriteIndented = true }));
    }

    private static WallType FirstBasicWallType(Document document) =>
        new FilteredElementCollector(document)
            .OfClass(typeof(WallType))
            .Cast<WallType>()
            .First(type => type.Kind == WallKind.Basic);

    private static WallType DuplicateWallTypeIfRequired(WallType source, string name)
    {
        Document document = source.Document;
        WallType? existing = new FilteredElementCollector(document)
            .OfClass(typeof(WallType))
            .Cast<WallType>()
            .FirstOrDefault(type => type.Name == name);
        return existing ?? (WallType)source.Duplicate(name);
    }

    private static FloorType DuplicateFloorTypeIfRequired(FloorType source, string name)
    {
        Document document = source.Document;
        FloorType? existing = new FilteredElementCollector(document)
            .OfClass(typeof(FloorType))
            .Cast<FloorType>()
            .FirstOrDefault(type => type.Name == name);
        return existing ?? (FloorType)source.Duplicate(name);
    }

    private static Wall CreateWall(
        Document document,
        XYZ start,
        XYZ end,
        WallType type,
        Level level,
        double height) =>
        Wall.Create(document, Line.CreateBound(start, end), type.Id, level.Id, height, 0, false, false);

    private static CurveLoop RectangleLoop(XYZ p00, XYZ p10, XYZ p11, XYZ p01)
    {
        CurveLoop loop = new();
        loop.Append(Line.CreateBound(p00, p10));
        loop.Append(Line.CreateBound(p10, p11));
        loop.Append(Line.CreateBound(p11, p01));
        loop.Append(Line.CreateBound(p01, p00));
        return loop;
    }

    private static FamilyInstance? PlaceHostedFamily(
        Document document,
        string familyPath,
        XYZ point,
        Wall host,
        Level level)
    {
        FamilySymbol? symbol = LoadFirstSymbol(document, familyPath);
        if (symbol is null)
        {
            return null;
        }

        if (!symbol.IsActive)
        {
            symbol.Activate();
            document.Regenerate();
        }

        return document.Create.NewFamilyInstance(point, symbol, host, level, StructuralType.NonStructural);
    }

    private static FamilyInstance? PlaceFreeFamily(
        Document document,
        string familyPath,
        XYZ point,
        Level level)
    {
        FamilySymbol? symbol = LoadFirstSymbol(document, familyPath);
        if (symbol is null)
        {
            return null;
        }

        if (!symbol.IsActive)
        {
            symbol.Activate();
            document.Regenerate();
        }

        return document.Create.NewFamilyInstance(point, symbol, level, StructuralType.NonStructural);
    }

    private static FamilySymbol? LoadFirstSymbol(Document document, string familyPath)
    {
        if (!File.Exists(familyPath) || !document.LoadFamily(familyPath, out Family family))
        {
            return null;
        }

        ElementId symbolId = family.GetFamilySymbolIds().First();
        return document.GetElement(symbolId) as FamilySymbol;
    }

    private static void SetUpperLimit(Room room, Level upperLevel)
    {
        Parameter? upper = room.get_Parameter(BuiltInParameter.ROOM_UPPER_LEVEL);
        if (upper is { IsReadOnly: false })
        {
            upper.Set(upperLevel.Id);
        }
    }

    private static void SetText(Parameter? parameter, string value)
    {
        if (parameter is { IsReadOnly: false })
        {
            parameter.Set(value);
        }
    }

    private static void SetInteger(Parameter? parameter, int value)
    {
        if (parameter is { IsReadOnly: false })
        {
            parameter.Set(value);
        }
    }

    private static double ToFeet(double metres) => UnitUtils.ConvertToInternalUnits(metres, UnitTypeId.Meters);

    private static string Sha256(string path)
    {
        using SHA256 algorithm = SHA256.Create();
        using FileStream stream = new(
            path,
            FileMode.Open,
            FileAccess.Read,
            FileShare.ReadWrite | FileShare.Delete);
        return Convert.ToHexString(algorithm.ComputeHash(stream)).ToLowerInvariant();
    }

    private static void Log(string path, string message) =>
        File.AppendAllText(path, $"{DateTimeOffset.Now:O} {message}{Environment.NewLine}");

    private sealed record ExportRecord(
        string Name,
        string IfcVersion,
        int SpaceBoundaryLevel,
        bool Status,
        string? Path,
        string? Sha256,
        string? Error);
}
