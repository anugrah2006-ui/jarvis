
# === New Code ===
Okay, please provide the task you want the HTML code for. I need to know what the HTML should display or do in order to write the code for you.

For example, tell me:

*   **What is the purpose of the HTML?** (e.g., display a form, create a landing page, show a list of items, etc.)
*   **What elements do you need?** (e.g., headings, paragraphs, images, links, forms, lists, tables, etc.)
*   **Any specific styling requirements?** (e.g., colors, fonts, layout, responsiveness)
*   **Do you need any JavaScript interaction?** (e.g., form validation, dynamic content updates)
*   **Any specific IDs or Classes for elements?** (This helps with styling and JavaScript interaction).

**Example of a Task:**

"Create a simple HTML page with a heading, a paragraph of text, and an image. The heading should say 'My Awesome Page', the paragraph should be a brief introduction, and the image should be a picture of a cat. The page should have a title 'Awesome Page' and a white background."

Once you provide the task, I will give you the clean, readable HTML code.


# === New Code ===
Okay, please provide the task you want me to write the HTML code for. For example, tell me:

*   **What should the HTML page display?** (e.g., a form, a list of items, a paragraph of text, an image gallery)
*   **What elements should be included?** (e.g., headings, paragraphs, input fields, buttons, images, links)
*   **Any specific formatting or layout requirements?** (e.g., should it be responsive, should it have a specific color scheme?)
*   **Any interactivity required?** (e.g., should it include JavaScript for handling events?)
*   **If it's part of a larger system or framework, please provide those details as well.**

Once you provide me with the details of the task, I'll write clean and readable HTML code for you.

**Example Prompt:**

"Write HTML code for a simple contact form. It should include fields for name, email, and message, and a submit button.  Include appropriate labels for each field. Make the form responsive, so the fields stack vertically on smaller screens."

**Example Response (Based on the above prompt):**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Form</title>
    <style>
        /* Basic styling for responsiveness */
        body {
            font-family: sans-serif;
            margin: 20px;
        }

        form {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        label {
            display: block;
            margin-bottom: 5px;
        }

        input[type="text"],
        input[type="email"],
        textarea {
            width: 100%;
            padding: 8px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box; /* Ensures padding doesn't affect width */
        }

        textarea {
            height: 150px;
        }

        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #3e8e41;
        }

        /* Media query for smaller screens */
        @media (max-width: 600px) {
            form {
                padding: 10px;
            }
        }
    </style>
</head>
<body>

    <form action="#" method="post">  <!-- Replace '#' with your form submission URL -->
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>

        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required>

        <label for="message">Message:</label>
        <textarea id="message" name="message" required></textarea>

        <button type="submit">Submit</button>
    </form>

</body>
</html>
```

I've included basic CSS styling in the `<style>` tag within the `<head>` to provide a basic responsive layout. Remember to replace `#` in the `action` attribute with the appropriate URL for your form submission handler.

Now, please provide your task so I can give you the best possible HTML code!

