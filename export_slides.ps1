$pptxPath = (Resolve-Path "AgriTwinX_Final_Project_Review.pptx").Path
$outDir = Join-Path (Get-Location) "exported_slides"
if (!(Test-Path $outDir)) { 
    New-Item -ItemType Directory -Path $outDir | Out-Null
}

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
$slideCount = $pres.Slides.Count

for ($i = 1; $i -le $slideCount; $i++) {
    $slideName = "slide_" + $i.ToString("D2") + ".png"
    $outPng = Join-Path $outDir $slideName
    $pres.Slides.Item($i).Export($outPng, "PNG", 1920, 1080)
}

$pres.Close()
$ppt.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
Write-Host "Successfully exported $slideCount slides to $outDir"

