# Rockae.Domain.WebAPI

### **2. Database Schema (Entity Names)**

#### **User Table**
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| `user_id` | INT | PRIMARY KEY, AUTO_INCREMENT |
| `username` | VARCHAR(255) | UNIQUE, NOT NULL |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL |
| `password` | VARCHAR(255) | NOT NULL |
| `isactive` | BOOLEAN | NOT NULL |

#### **UserProfile Table**
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| `profile_id` | INT | PRIMARY KEY, AUTO_INCREMENT |
| `user_id` | INT | FOREIGN KEY REFERENCES User(userid), UNIQUE, NOT NULL |
| `firstname` | VARCHAR(100) | NOT NULL |
| `lastname` | VARCHAR(100) | NOT NULL |
| `phone` | VARCHAR(20) | NULLABLE |
| `date_of_birth` | DATE | NULLABLE |
| `bio` | TEXT | NULLABLE |

#### **QuizPool Table**
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| `quiz_id` | INT | PRIMARY KEY, AUTO_INCREMENT |
| `quiz_title` | VARCHAR(255) | NOT NULL |
| `user_id` | INT | FOREIGN KEY REFERENCES User(userid), NOT NULL |
| `create_date` | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| `candidate_auth_required` | BOOLEAN | NOT NULL |

#### **QuizQuestion Table**
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| `question_id` | INT | PRIMARY KEY, AUTO_INCREMENT |
| `quiz_id` | INT | FOREIGN KEY REFERENCES Quiz_Created(quiz_id), NOT NULL |
| `question_text` | TEXT | NOT NULL |
| `answer_a` | VARCHAR(255) | NOT NULL |
| `answer_b` | VARCHAR(255) | NOT NULL |
| `answer_c` | VARCHAR(255) | NOT NULL |
| `answer_d` | VARCHAR(255) | NOT NULL |
| `correct_answer` | VARCHAR(1) | CHECK (correct_answer IN ('A', 'B', 'C', 'D')) |

#### **QuizResult Table**
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| `test_id` | INT | PRIMARY KEY, AUTO_INCREMENT |
| `quiz_id` | INT | FOREIGN KEY REFERENCES Quiz_Created(quiz_id), NOT NULL |
| `candidate_name` | VARCHAR(255) | NOT NULL |
| `candidate_app_id` | VARCHAR(255)
| `completion_date` | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| `score` | INT | CHECK (score BETWEEN 0 AND 100) |

#### **API Rate Limiting Table**
| Column Name | Data Type | Constraints |
|-------------|-----------|-------------|
| `api_id` | INT | PRIMARY KEY, AUTO_INCREMENT |
| `user_id` | INT | FOREIGN KEY REFERENCES User(userid), NOT NULL |
| `request_count` | INT | DEFAULT 0 |
| `last_request_time` | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### **3. API Endpoints**

#### **Authentication & User Management**
- `POST /api/register/` – Register a new user in User Table
- `POST /api/login/` – Authenticate from User table and return JWT token
- `GET /api/user/profile/` – Retrieve user profile from UserProfile Table
- `PUT /api/user/profile/` – Update user profile in UserProfile Table
- `POST /api/user/profile/` – Create user profile in UserProfile Table

#### **Quiz Management**
- `POST /api/quiz/` – Create a new quiz in QuizPool Table
- `GET /api/quiz/{quiz_id}/` – Retrieve quiz details from QuizPool Table
- `DELETE /api/quiz/{quiz_id}/` – Delete a quiz from QuizPool Table

#### **Quiz Question Management**
- `POST /api/quiz/{quiz_id}/question/` – Add a question to a quiz
- `GET /api/quiz/{quiz_id}/questions/` – Retrieve all questions for a quiz
- `GET /api/quiz/{quiz_id}/question/{question_id}/` – Get a question
- `DELETE /api/quiz/{quiz_id}/question/{question_id}/` – Delete a question

#### **Test Management**
- `POST /api/test/{quiz_id}/` – Start a test
- `GET /api/test/{test_id}/` – Retrieve test details
- `POST /api/test/{test_id}/submit/` – Submit answers for scoring

#### **API Rate Limiting**
- `GET /api/rate_limit/` – Check API usage count
- `POST /api/rate_limit/reset/` – Reset API usage count (admin only)

### **4. Security Measures**
- **JWT Authentication:** Secure user authentication
- **Rate Limiting:** Prevent excessive API calls
- **Data Validation:** Ensure data consistency
- **Role-Based Access Control:** Restrict actions based on user roles
