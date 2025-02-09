# Product Requirements Document (PRD)

## **Automating Apple Personal Voice Recording on macOS**

### **1. Overview**
This document outlines the requirements for a macOS-based automation tool that facilitates the creation of **Apple Personal Voice** using **TTS output from another system**. The tool will extract **OCR text from Apple's Personal Voice UI**, automate **button presses**, and play the extracted text using TTS to simulate a real user completing the Personal Voice training.

---

## **2. Objectives**
- Enable users to **migrate an existing synthetic voice** into Apple’s Personal Voice system.
- Automate the **entire Personal Voice training process**, removing the need for manual intervention.
- Leverage **macOS automation tools** (AppleScript, Shortcuts, OCR, and UI scripting) for seamless execution.
- Ensure **high accuracy** in text extraction and playback synchronization.

---

## **3. Key Features & Functionality**

| Feature | Description |
|---------|------------|
| **OCR-Based Text Extraction** | Uses Apple’s **Vision framework** to extract the prompt displayed by Personal Voice. |
| **Automated Button Pressing** | Utilizes **AppleScript and UI Scripting** to simulate clicking “Record” and “Continue” buttons. |
| **TTS Playback of Extracted Prompts** | Uses an external **TTS engine** (e.g., Speak for Yourself, macOS built-in `say` command, or another tool) to read out the extracted text. |
| **Loop Until Completion** | The automation will **repeat the process** until all prompts have been recorded. |
| **Adjustable Delay Handling** | Introduces **customizable pauses** between actions to ensure smooth operation. |

---

## **4. User Workflow**

1. **Launch the Automation**
   - User runs the automation script via **a macOS Shortcut, AppleScript, or CLI command**.
   - The system checks if **Personal Voice setup is open**.
   
2. **Capture the Prompt Text**
   - The script takes a **screenshot** of the screen region displaying the text prompt.
   - OCR processes the image and extracts the text.
   - The extracted text is stored **in a text file or variable**.

3. **Trigger the Recording**
   - The script **simulates a button press** on the “Record” button.
   - Waits for **1-2 seconds** to ensure the system is ready.

4. **Playback the Prompt via TTS**
   - The extracted text is **fed into a TTS engine**.
   - The voice output is played **through the system microphone** (or via a loopback input).

5. **Click “Continue” After Playback**
   - After the playback finishes, the script **simulates pressing the “Continue” button**.

6. **Repeat Until All Prompts Are Processed**
   - The script repeats the process until **all prompts have been recorded**.

---

## **5. Technical Approach**

### **5.1 OCR Implementation**
#### **Using Apple’s Vision Framework**
- Uses `VNRecognizeTextRequest` to extract text from images.
- Extracted text is processed and stored in a variable.

#### **Example Code for OCR in AppleScript**
```applescript
on extractTextFromImage(imagePath)
    set imgURL to current application's NSURL's fileURLWithPath:imagePath
    set img to current application's NSImage's alloc()'s initWithContentsOfURL:imgURL
    set imgRef to img's CGImageForProposedRect:(missing value) context:(missing value) hints:(missing value)
    
    if imgRef = missing value then
        display dialog "Error: Failed to convert image"
        return ""
    end if
    
    set request to current application's VNRecognizeTextRequest's alloc()'s init()
    request's setRecognitionLevel:(current application's VNRequestTextRecognitionLevelAccurate)
    request's setUsesLanguageCorrection:true
    request's setRecognitionLanguages:{"en"}
    
    set handler to current application's VNImageRequestHandler's alloc()'s initWithCGImage:imgRef options:(missing value)
    handler's performRequests:{request} |error|:(missing value)
    
    set observations to request's results()
    set extractedText to {}
    repeat with observation in observations
        set text to (observation's topCandidates:1)'s firstObject()'s string()
        set end of extractedText to text
    end repeat
    
    return extractedText as text
end extractTextFromImage
```

---

### **5.2 UI Automation**
#### **Simulating “Record” Button Click**
```applescript
tell application "System Events"
    tell process "System Preferences"
        click button "Record" of window 1
    end tell
end tell
```

#### **Simulating “Continue” Button Click**
```applescript
tell application "System Events"
    tell process "System Preferences"
        click button "Continue" of window 1
    end tell
end tell
```

---

## **6. Edge Cases & Solutions**

| **Scenario** | **Proposed Solution** |
|-------------|----------------------|
| OCR fails to extract text | Retry OCR after a brief delay (5 sec). |
| Personal Voice UI changes | Use **UI automation detection** to adjust. |
| TTS playback cuts off | Add **custom delays** to ensure full playback. |
| Record/Continue buttons don’t register | Implement **keyboard shortcuts as fallback**. |

---

## **7. Security & Compliance**
- The tool will run **entirely on-device**, ensuring privacy.
- No data is **stored or transmitted** externally.
- The script will use **macOS Accessibility permissions**, requiring user approval.

---

## **8. Deployment Plan**

| **Phase** | **Task** |
|----------|---------|
| **Phase 1: Prototype** | Build a script to automate OCR, button clicks, and TTS playback. |
| **Phase 2: Testing** | Run on multiple macOS versions, test with different UI layouts. |
| **Phase 3: User Beta** | Allow testers to verify the automation on real Personal Voice setups. |
| **Phase 4: Final Release** | Package as a macOS Shortcut or standalone script. |

---

## **9. Open Questions**
- Can we **detect** when Personal Voice moves to a new prompt automatically?
- Should we use **a UI monitoring tool** to detect UI state changes instead of relying on time delays?
- Are there **Apple API hooks** that allow submitting pre-recorded clips instead of recording them live?

---

## **10. Conclusion**
This tool provides a **fully automated** method for migrating an existing synthetic voice into **Apple’s Personal Voice**. By leveraging **OCR, UI automation, and TTS playback**, it eliminates manual intervention while ensuring high accuracy. Future improvements may include **direct API integration** if Apple introduces it.

