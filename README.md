[![alt-text](https://img.shields.io/github/repo-size/Phongtran1201/knowledge)](https://github.com/Phongtran1201/Knowledge.git)
[![alt-text](https://img.shields.io/github/languages/top/Phongtran1201/knowledge)](https://github.com/Phongtran1201/Knowledge.git)
[![alt-text](https://img.shields.io/maintenance/no/2022)](https://github.com/Phongtran1201/Knowledge.git)
[![alt-text](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fexmple.com)](https://github.com/Phongtran1201/Knowledge.git)
[![alt-text](https://img.shields.io/github/followers/Phongtran1201?style=social)](https://github.com/Phongtran1201/Knowledge.git)

# Knowledge Management


<!-- [![website](./images/instagram.svg)](example.com) -->
<!-- &nbsp;&nbsp; -->
---
## Example C Program: Verifying the Signature of a PE File

The `WinVerifyTrust` API can be used to verify the signature of a portable executable file.

The following example shows how to use the `WinVerifyTrust` API to verify the signature of a signed portable executable file.



```c
//-------------------------------------------------------------------
// Copyright (C) Microsoft.  All rights reserved.
// Example of verifying the embedded signature of a PE file by using 
// the WinVerifyTrust function

#include <tchar.h>
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <Softpub.h>
#include <wincrypt.h>
#include <wintrust.h>


#define _UNICODE 1
#define  UNICODE 1
// Link with the Wintrust.lib file.
#pragma comment (lib, "wintrust")

BOOL VerifyEmbeddedSignature(LPCWSTR pwszSourceFile) {
    
    LONG lStatus;
    DWORD dwLastError;

    // Initialize the WINTRUST_FILE_INFO structure.

    WINTRUST_FILE_INFO FileData;
    memset(&FileData, 0, sizeof(FileData));
    FileData.cbStruct = sizeof(WINTRUST_FILE_INFO);
    FileData.pcwszFilePath = pwszSourceFile;
    FileData.hFile = NULL;
    FileData.pgKnownSubject = NULL;

    GUID WVTPolicyGUID = WINTRUST_ACTION_GENERIC_VERIFY_V2;
    WINTRUST_DATA WinTrustData;

    // Initialize the WinVerifyTrust input data structure.

    // Default all fields to 0.
    memset(&WinTrustData, 0, sizeof(WinTrustData));

    WinTrustData.cbStruct = sizeof(WinTrustData);

    // Use default code signing EKU.
    WinTrustData.pPolicyCallbackData = NULL;

    // No data to pass to SIP.
    WinTrustData.pSIPClientData = NULL;

    // Disable WVT UI.
    WinTrustData.dwUIChoice = WTD_UI_NONE;

    // No revocation checking.
    WinTrustData.fdwRevocationChecks = WTD_REVOKE_NONE;

    // Verify an embedded signature on a file.
    WinTrustData.dwUnionChoice = WTD_CHOICE_FILE;

    // Verify action.
    WinTrustData.dwStateAction = WTD_STATEACTION_VERIFY;

    // Verification sets this value.
    WinTrustData.hWVTStateData = NULL;

    // Not used.
    WinTrustData.pwszURLReference = NULL;

    // This is not applicable if there is no UI because it changes 
    // the UI to accommodate running applications instead of 
    // installing applications.
    WinTrustData.dwUIContext = 0;

    // Set pFile.
    WinTrustData.pFile = &FileData;

    // WinVerifyTrust verifies signatures as specified by the GUID 
    // and Wintrust_Data.
    lStatus = WinVerifyTrust(
        NULL,
        &WVTPolicyGUID,
        &WinTrustData);

    switch (lStatus)
    {
    case ERROR_SUCCESS:
        /*
        Signed file:
            - Hash that represents the subject is trusted.

            - Trusted publisher without any verification errors.

            - UI was disabled in dwUIChoice. No publisher or
                time stamp chain errors.

            - UI was enabled in dwUIChoice and the user clicked
                "Yes" when asked to install and run the signed
                subject.
        */
        wprintf_s(L"[*] - The file \"%s\" is signed and the signature "
            L"was verified.\n",
            pwszSourceFile);
        break;

    case TRUST_E_NOSIGNATURE:
        // The file was not signed or had a signature 
        // that was not valid.

        // Get the reason for no signature.
        dwLastError = GetLastError();
        if (TRUST_E_NOSIGNATURE == dwLastError ||
            TRUST_E_SUBJECT_FORM_UNKNOWN == dwLastError ||
            TRUST_E_PROVIDER_UNKNOWN == dwLastError)
        {
            // The file was not signed.
            wprintf_s(L"[*] - The file \"%s\" is not signed.\n",
                pwszSourceFile);
            return false;
        }
        else
        {
            // The signature was not valid or there was an error 
            // opening the file.
            wprintf_s(L"[*] - An unknown error occurred trying to "
                L"verify the signature of the \"%s\" file.\n",
                pwszSourceFile);
            return false;
        }

        break;

    case TRUST_E_EXPLICIT_DISTRUST:
        // The hash that represents the subject or the publisher 
        // is not allowed by the admin or user.
        wprintf_s(L"[*] - The signature is present, but specifically "
            L"disallowed.\n");
        break;

    case TRUST_E_SUBJECT_NOT_TRUSTED:
        // The user clicked "No" when asked to install and run.
        wprintf_s(L"[*] - The signature is present, but not "
            L"trusted.\n");
        break;

    case CRYPT_E_SECURITY_SETTINGS:
        /*
        The hash that represents the subject or the publisher
        was not explicitly trusted by the admin and the
        admin policy has disabled user trust. No signature,
        publisher or time stamp errors.
        */
        wprintf_s(L"[*] - CRYPT_E_SECURITY_SETTINGS - The hash "
            L"representing the subject or the publisher wasn't "
            L"explicitly trusted by the admin and admin policy "
            L"has disabled user trust. No signature, publisher "
            L"or timestamp errors.\n");
        break;

    default:
        // The UI was disabled in dwUIChoice or the admin policy 
        // has disabled user trust. lStatus contains the 
        // publisher or time stamp chain error.
        wprintf_s(L"[-.-] - Error is: 0x%x.\n",
            lStatus);
        return false;
    }

    // Any hWVTStateData must be released by a call with close.
    WinTrustData.dwStateAction = WTD_STATEACTION_CLOSE;

    lStatus = WinVerifyTrust(
        NULL,
        &WVTPolicyGUID,
        &WinTrustData);

    return true;
}

```

---
## Searches a directory for a file or subdirectory

> [fileapi.h](https://docs.microsoft.com/en-us/windows/win32/api/fileapi/)

```c
wchar_t currentPath[] = { '.','\\','*',0 };

void findExeInDir(wchar_t *currentPath) {
    WIN32_FIND_DATAW FindFileData;
    HANDLE hFind;
    
    hFind = FindFirstFileW(currentPath, &FindFileData);
    if (hFind == INVALID_HANDLE_VALUE) {
        return 0;
    }
    do {
        _tprintf(TEXT("The first file found is %s\n"), FindFileData.cFileName);

    } while (FindNextFileW(hFind, &FindFileData) != 0);
}
```
---
## Check file exists or not

```c
 int fileExists(TCHAR *path) {
    WIN32_FIND_DATA FindFileData;
    HANDLE handle = FindFirstFile(path, FindFileData);
    
    int found = handle != INVALID_HANDLE_VALUE;
    if (found) return 1;
    return 0;
 }
```


