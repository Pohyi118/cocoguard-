param([int]$Rate = 1)
Add-Type -AssemblyName System.Speech
$dir = "C:\Users\User\Documents\GSC\video\audio"
foreach ($i in 1..8) {
  $s = New-Object System.Speech.Synthesis.SpeechSynthesizer
  $s.SelectVoice("Microsoft Zira Desktop"); $s.Rate = $Rate
  $s.SetOutputToWaveFile("$dir\s$i.wav")
  $s.Speak((Get-Content "$dir\s$i.txt" -Raw -Encoding UTF8)); $s.Dispose()
}
