# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
One edge case is when a user creates a student but does not include a `mark` in the request body.


2) How you have accounted for this in your implementation
In my implementation, `mark` is optional for `POST /students`. If it is not provided, I store the student with a default mark of `0`.
This follows the project specification, which says that `mark` is optional when creating a student.  
Choosing `0` keeps the response structure consistent and ensures the `/stats` endpoint can still calculate values without needing extra handling for missing marks.