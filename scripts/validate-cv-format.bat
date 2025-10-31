@echo off
REM CV Format Validation Script (Windows)
REM Validates CV PDF formatting against master CV standards
REM Usage: validate-cv-format.bat <path-to-cv.pdf>

setlocal enabledelayedexpansion

set "PDF_PATH=%~1"
set "MAX_PAGES=2"
set "MIN_SIZE_KB=40"
set "MAX_SIZE_KB=100"

echo ========================================
echo    CV FORMAT VALIDATION TOOL
echo ========================================
echo.

if "%PDF_PATH%"=="" (
    echo [ERROR] No PDF file specified
    echo Usage: %0 ^<path-to-cv.pdf^>
    exit /b 1
)

if not exist "%PDF_PATH%" (
    echo [ERROR] PDF file not found: %PDF_PATH%
    exit /b 1
)

echo Validating: %PDF_PATH%
echo.

REM ============================================
REM CHECK 1: File Existence
REM ============================================
echo [1/4] Checking file existence...
if exist "%PDF_PATH%" (
    echo [PASS] PDF file exists
) else (
    echo [FAIL] PDF file not found
    exit /b 1
)
echo.

REM ============================================
REM CHECK 2: File Size
REM ============================================
echo [2/4] Checking file size...
for %%F in ("%PDF_PATH%") do set "FILE_SIZE_BYTES=%%~zF"
set /a "FILE_SIZE_KB=!FILE_SIZE_BYTES! / 1024"

echo    File size: !FILE_SIZE_KB!KB

if !FILE_SIZE_KB! LSS %MIN_SIZE_KB% (
    echo [FAIL] File too small ^(!FILE_SIZE_KB!KB ^< %MIN_SIZE_KB%KB^)
    echo        This suggests wrong template was used ^(not Eisvogel^)
    set "HAS_ERRORS=1"
) else if !FILE_SIZE_KB! GTR %MAX_SIZE_KB% (
    echo [WARN] File larger than expected ^(!FILE_SIZE_KB!KB ^> %MAX_SIZE_KB%KB^)
) else (
    echo [PASS] File size acceptable
)
echo.

REM ============================================
REM CHECK 3: Manual Verification Required
REM ============================================
echo [3/4] Manual verification required...
echo Please verify the following manually:
echo.
echo 1. Open %PDF_PATH%
echo 2. Check page count: Must be %MAX_PAGES% pages or less
echo 3. Check paper size: Should be A4
echo 4. Check formatting: Compare with master CV
echo.

REM ============================================
REM CHECK 4: Markdown Check (if .md exists)
REM ============================================
echo [4/4] Checking for markdown file...
set "MD_PATH=%PDF_PATH:.pdf=.md%"

if exist "%MD_PATH%" (
    echo    Found markdown: %MD_PATH%
    echo    Checking YAML...

    findstr /C:"documentclass:" "%MD_PATH%" >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo [FAIL] Found 'documentclass:' - DO NOT USE
        set "HAS_ERRORS=1"
    )

    findstr /C:"header-includes:" "%MD_PATH%" >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo [FAIL] Found 'header-includes:' - DO NOT USE
        set "HAS_ERRORS=1"
    )

    findstr /C:"geometry:" "%MD_PATH%" >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo [FAIL] Found 'geometry:' settings - DO NOT USE
        set "HAS_ERRORS=1"
    )

    if not defined HAS_ERRORS (
        echo [PASS] Markdown YAML looks clean
    )
) else (
    echo [SKIP] No markdown file found
)
echo.

REM ============================================
REM SUMMARY
REM ============================================
echo ========================================
echo    VALIDATION SUMMARY
echo ========================================
echo.

if defined HAS_ERRORS (
    echo [FAIL] CV has formatting issues
    echo.
    echo REMEDIATION STEPS:
    echo 1. Check markdown YAML - remove documentclass, header-includes, geometry
    echo 2. Ensure pandoc command uses: --template eisvogel
    echo 3. Regenerate PDF with correct settings
    echo 4. Run this validator again
    echo.
    echo Reference: applications\2025-11-VirginAtlantic-DigitalProductLead\ArturSwadzba_CV_VirginAtlantic.pdf
    exit /b 1
) else (
    echo [PASS] Basic validation passed
    echo.
    echo IMPORTANT: Complete manual verification:
    echo - Page count must be 2 pages or less
    echo - Paper size must be A4
    echo - Compare formatting with master CV
    exit /b 0
)
