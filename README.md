# keypr_task

## API:
| Method        | URL           | Description  | Data Parameters |
| ------------- | ------------- | ------------ | ------ |
| **GET** | `/reservations` |  Load all reservations | |
| **POST** | `/reservations` |  Add new reservation | last_name, first_name, room_number, start_date, end_date |
| **GET** | `/reservations/:id` |  Load reservation |  |
| **PUT** | `/reservations/:id` |  Update reservation | last_name, first_name, room_number, start_date, end_date |
| **DELETE** | `/reservations/:id` |  Delete reservation | |
| **GET** | `/reservations?start_date_range=<date>&end_date_range=<date>` |  Filter any reservation which has stay days inside range | |