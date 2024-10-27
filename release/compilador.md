# Compilado

- El programa fue compilado con el siguiente comando:

```ps1
nuitka --standalone --enable-plugin=tk-inter --windows-icon-from-ico=sources\app.ico --include-package=cv2 --include-package=customtkinter --include-package=threading --include-package=pathlib --include-package=random --include-package=string --include-package=tkinter --include-package=util.list --windows-console-mode=disable --output-filename=cutter.exe --nofollow-import-to=tkinter.test App.py
```

- Y el instalador se configuró con Inno Setup:

```inoscr
; Script mejorado para Inno Setup
; Configuración para el instalador de "Cutter"

#define MyAppName "Cutter"
#define MyAppVersion "1.0.1"
#define MyAppPublisher "baa4ts"
#define MyAppURL "https://github.com/Carlos-dev-G/cutter"
#define MyAppExeName "cutter.exe"
#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt ".myp"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
; Información básica del programa
AppId={{1CFD7732-11B1-4178-B53D-35AF44D8C7E1}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
OutputDir=C:\Users\baa4t\Desktop
OutputBaseFilename=instalador_cutter
SetupIconFile=C:\Users\baa4t\Documents\cutter\sources\app.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ChangesAssociations=no

; Compatibilidad del instalador
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
DisableProgramGroupPage=yes
LicenseFile=C:\Users\baa4t\Documents\cutter\LICENSE

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Incluye el ejecutable y todos los archivos en App.dist
Source: "C:\Users\baa4t\Documents\cutter\App.dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\baa4t\Documents\cutter\App.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Crea accesos directos en el menú de inicio y en el escritorio
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Ejecuta el programa después de la instalación si se selecciona
Filename: "{app}\{#MyAppExeName}"; Description: "Ejecutar {#MyAppName}"; Flags: nowait postinstall skipifsilent
```