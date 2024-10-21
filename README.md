# Expense Sharing Application

## Overview
The Expense Sharing Application allows users to track and share expenses with others. Users can create expenses, split them equally or by specific amounts/percentages, and view their personal and shared expenses.
Note : this is backend only

## Features
- User authentication and profile management.
- Create and manage expenses.
- Split expenses equally, by exact amounts, or by percentages.
- Retrieve personal and overall expenses.
- Download expenses as a CSV file.

## Models

### Profile
- `user`: OneToOneField (User)
- `phone`: CharField
- `email`: EmailField
- `name`: CharField

### Expense
- `item_service`: CharField
- `cost`: DecimalField
- `creator`: ForeignKey (Profile)
- `participants`: ManyToManyField (Profile)
- `split_method`: CharField
- `created_at`: DateTimeField (auto_now_add)

### Note: Creator is also a participant
### ParticipantExpense
- `expense`: ForeignKey (Expense)
- `profile`: ForeignKey (Profile)
- `amount_owed`: DecimalField
# API Endpoints
## Main APIS
`main/views.py`
### Create Expense
- **URL**: `/expense`
- **Method**: POST
- **Request Body**:
- for equal splits
  ```json
  {
    "service": "Restaurant",
    "amount": 25.0,
    "split_type": "equal",
    "participants": ["user1", "user2"]
  }
### Get personal Expenses
- **URL**: `/expenses`
- **Method**: GET
- **Response Body**:
 ```json
    {
  "expenses": [
    {
      "service_name": "Restaurant",
      "amount_owed": 12.5,
      "date_timestamp": "2024-01-01T12:00:00Z"
    }
  ]
}
```
### Download CSV
- **URL**: `/download_csv`
- **Method**: GET
### Get overall expenses
- **URL**: `/overall_expenses`
- **Method**: GET
### Download CSV
- **URL**: `/download_overall_csv`
- **Method**: GET


## Validation api endpoints
`validation/views.py`
- POST API `(“/equalsplit”)`
- POST API `(“/validpercentages”)`
- POST API `(“/validamounts”)`
### Validation utility functions:
- `EqualSplit(amount,n)`: return a list of n contributions each of worth:amount/n 
- `ValidPercentages(list of percentages)`:return true if sum equal to 100
- `ValidAmounts(total,list of contributions)`: return true if sum of contributions is equal to 100

## Authentication Apis: 
`accounts/views.py`
Authentication using Django inbuilt auth. Csrf sookies
-	Signup `(“/signup”)`
-	Login `(“/login”)`
-	Logout `(“/logout”)`
-	Search for profile based on username`(”/profiles”)`
