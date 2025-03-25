# AstroMood Acceptance Tests and Acceptance Criteria Document

Sümeyye Sıla Altay 231101077  
Esmanur Ulu 231101024  
Zeynep Yetkin 231101042  
Hazal Epözdemir 231101037

---

## Table of Contents
1. [Document Specific Task Matrix](#document-specific-task-matrix)
2. [Introduction](#introduction)
3. [Acceptance Criteria](#acceptance-criteria)
   - [1. User Birth Date Input & Zodiac Calculation](#1-user-birth-date-input--zodiac-calculation)
   - [2. Mood Input](#2-mood-input)
   - [3. Personalized Recommendations](#3-personalized-recommendations)
   - [4. Quote & Motivation Message Generator](#4-quote--motivation-message-generator)
4. [Acceptance Tests](#acceptance-tests)
5. [Mapping to Use Cases](#mapping-to-use-cases)
6. [Appendices](#appendices)

---

## Document Specific Task Matrix

| Task                         | Team Member Responsible                |
|------------------------------|----------------------------------------|
| Defining Acceptance Criteria | Hazal Epözdemir, Sümeyye Sıla Altay      |
| Acceptance Tests             | Zeynep Yetkin, Esmanur Ulu               |

---

## Introduction

This document contains the acceptance criteria defined for the four selected scenarios in the AstroMood project demo and the acceptance tests prepared based on these criteria. The tests aim to verify whether the project meets its functional and non-functional requirements.

---

## Acceptance Criteria

The acceptance criteria for the four main scenarios of the project are as follows:

### 1. User Birth Date Input & Zodiac Calculation
- The system must correctly calculate the zodiac sign based on the user's birth date.
- The calculation time must not exceed 4 seconds.
- If the user enters an invalid or incorrectly formatted date, the system should display an appropriate error message indicating the issue.

### 2. Mood Input
- The user must be able to select their mood (today, yesterday, or tomorrow) and submit it.
- If the mood input is incomplete or missing, the system should display a clear error message prompting the user to provide the necessary information.

### 3. Personalized Recommendations
- The system must provide personalized recommendations (book, movie, TV series, and exercise) based on the user's zodiac sign and mood.
- If the required mood or zodiac sign is missing, the system should display an error message asking the user to provide valid input.

### 4. Quote & Motivation Message Generator
- Motivational quotes and messages should be relevant to the user’s mood and displayed correctly.
- The content provided must be up-to-date and in real-time.

---

## Acceptance Tests

| Scenario                                       | Test Name                      | Preconditions                                               | Test Steps                                                                                                                                           | Expected Outcome (Correct Input)                                                                                                                                                       | Expected Outcome (Invalid Input)                                                                |
|------------------------------------------------|--------------------------------|-------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| 1-User Birth Date Input & Zodiac Calculation   | Correct Zodiac Calculation     | Website is operational, internet connection is available    | 1. The user enters their birth date on the homepage.<br>2. Clicks the "Calculate" button.                                                           | The system correctly calculates and displays the zodiac sign based on the entered date. The calculation does not exceed 4 seconds.                                                      | An error message is displayed indicating the incorrect format or invalid birth date.             |
| 2-Mood Input Form Validation                   | Mood Entry Validation          | Website is operational, user had already selected the birth date | 1. The user opens the mood input form.<br>2. Selects today, yesterday, or tomorrow for mood analysis.<br>3. Clicks “Show Mood”                          | The system proceeds to show the mood analysis after the "Show Mood" button is clicked.                                                                                                  | If the required field is left empty, a clear error message prompts the user to fill in the missing field. |
| 3-Personalized Recommendations                 | Personalized Suggestions       | The user has entered their mood, and the zodiac sign has been correctly calculated. | 1. The user selects the mood and what type of recommendations they want.                                                                           | The system displays book, movie, music, and activity recommendations based on the user's zodiac sign and mood. The accuracy of the recommendations must be at least 75%.            | If the required mood or zodiac sign is not selected, the system shows an error message asking for valid input. |
| 4-Quote & Motivation Message Generator         | Motivational Messages          | Website is operational, and the user has entered their mood.  | 1. The user clicks the "Display Quote" button.                                                                                                     | Motivational quotes and messages relevant to the user’s mood are displayed. The content is provided with the latest updates.                                                            | If the user hasn’t entered the mood or if there's an issue with the mood selection, an error message is displayed, or no motivational messages are shown. |

---

## Mapping to Use Cases

- **Birth Date Entry & Zodiac Calculation** → Scenario 1  
- **Mood Entry** → Scenario 2  
- **Personalized Recommendations** → Scenario 3  
- **Motivational Messages** → Scenario 4  

---

## Appendices

### Correct Zodiac Calculation test cases:

<img src="https://github.com/hazal327/AstroMood/blob/main/images/img1.png" width="400" />
<img src="https://github.com/hazal327/AstroMood/blob/main/images/img2.png" width="400" />
invalid input:
<img src="https://github.com/hazal327/AstroMood/blob/main/images/img5.png" width="400" />

### Mood Entry Validation test case:
<img src="https://github.com/hazal327/AstroMood/blob/main/images/img3.png" width="400" />

### Personalized Suggestions test cases:
<img src="https://github.com/hazal327/AstroMood/blob/main/images/img4.png" width="400" />
<img src="https://github.com/hazal327/AstroMood/blob/main/images/img7.png" width="400" />
invalid input:
<img src="https://github.com/hazal327/AstroMood/blob/main/images/img6.png" width="400" />

### Feedback System:


