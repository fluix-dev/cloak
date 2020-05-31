<p align=center>
    <img alt="Cloak Logo" src="misc/full_logo.png">
    <h3 align=center>An application platform that removes bias from the equation</h3>
</p>
<p align=center>
    <img alt="GitHub" src="https://img.shields.io/github/license/theaviddev/cloak">
    <a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_3.6-green.svg"></a>
    <img alt="Website" src="https://img.shields.io/website?down_color=red&down_message=offline&up_color=green&up_message=online&url=https%3A%2F%2Fcloak.theavid.dev">
    <img alt="Libraries.io dependency status for GitHub repo" src="https://img.shields.io/librariesio/github/theaviddev/cloak">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/theaviddev/cloak">
    <br>
    <a href="#about">About</a> | <a href="#features">Features</a> | <a href="#usage">Usage</a>
</p>

# About
Cloak is a form and application creation service that attempts to decrease the amount of bias that goes into applications. Often, people's subconcious biases will play a role in how well an applicant does and Cloak tries to eliminate this. It does so by hiding specified fields completely, until an application is accepted - at which point an email will be sent to the applicant. This ensures that form creators can still access data that they will need after accpetance, but makes sure that this isn't part of what determines whether someone makes it in or not.

The core functionality of Cloak resides in the Django open source Python web framework. It allows us to create flexible models, stored in a PostgreSQL database, without writing a single line of SQL. Through Django's admin pages, Cloak hides all personally identifiable information to remove potential bias from applications. Cloak is hosted on a dedicated server running an Nginx reverse proxy. Our fabulous domain name is provided by Namecheap with DigitalOcean acting as a nameserver and host. All traffic is secured through LetsEncrypt SSL certificates ensuring that your private data is safe.

*This project was made for MasseyHacks VI 2020 by [TheAvidDev](https://github.com/TheAvidDev/), [dulldesk](https://github.com/dulldesk/), and [skyflaren](https://github.com/skyflaren/).*

# Features
 - Automatic, NLP-based text summarization powered by [TextRank](https://github.com/summanlp/textrank).
 - Form access management with separate editor and reviwer roles.
 - Public application / form showcase to market your form.
 - JSON API to get your data anywhere you need it.
 - Automatic form closing, submission time tracking, and much more...

# Usage
To use Cloak, first sign up on our [site](https://cloak.theavid.dev). Then, go ahead and create a form. Feel free to add as many questions as you like of various types. Also remember that long answer questions will be automatically summarized to 100 words, with an option to view the full response on the individual response page. You can set the following parameters on the main form:
 - **Name** - A name for your form.
 - **Description** - A description about what your form is about.
 - **Open** - Whether your form is accepting submissions or not.
 - **Auto-Close Date** - A date and time to automatically close your form.
 - **Publicly Displayed** - Whether this form will be on our public display of forms or not.
 
Each form field or question also has the following parameters:
 - **Input Type** - The type of input, whether it's numeric, multiple coice, or long or short answer.
 - **Question** - A prompt or question for the user to know what to respond to.
 - **Required** - Whether this field is required or not.
 - **Secret** - Whether the response to this field will be kept completely hidden until this form is accepted. The recipient will also know whether a field is secret or not.
 - **Description** - A description or "extra information" section displayed below the question. Useful if you want answers in a particular format or want to clarify the question.
 - **Multiple Choice Choices** - One choice per line for each of the multiple choice options. Only applicable to Multiple Choice input types.

Finally, once you are done customizing your form, hit **Save and continue editing**. Then, click **View on Site** to view the form and get the link to send out to applications. And that's it! You've created a form with Cloak and can have the peace of mind that at least some bias is removed from your application process.

## JSON API
The API currently has the following endpoints that return data:
 - `/api/forms/public/` Returns a list of all the public forms, along with their `uuid`, `form_id`, and absolute url path after the domain. An example is shown below:
```json
$ curl https://cloak.theavid.dev/api/forms/public/ | jq

{
  "length": 3,
  "forms": [
    {
      "uuid": "f3d43289-6844-4829-93ce-1cb4b4c3f6e1",
      "form_id": "3gCSZMsdjBfiEQGJnkKROIh2CsMWq24fHz9Sr0-wJsBjDBCc8Hp8rP78PLfLPkaoBMB9vQ6MyhTot6_mlY6egg",
      "url": "/form/f3d43289-6844-4829-93ce-1cb4b4c3f6e1/3gCSZMsdjBfiEQGJnkKROIh2CsMWq24fHz9Sr0-wJsBjDBCc8Hp8rP78PLfLPkaoBMB9vQ6MyhTot6_mlY6egg/"
    },
    {
      "uuid": "62a02da2-cff4-4c54-9461-2a7b74a352f1",
      "form_id": "MeNq5Ph6qV3HXUSMZaB0vvM9xADDlUwTfDW5QsrY_7_4XXiImv6DOk6W9k-kM-MmjxrVf5UUfqOZMmaOPPEtgA",
      "url": "/form/62a02da2-cff4-4c54-9461-2a7b74a352f1/MeNq5Ph6qV3HXUSMZaB0vvM9xADDlUwTfDW5QsrY_7_4XXiImv6DOk6W9k-kM-MmjxrVf5UUfqOZMmaOPPEtgA/"
    },
    {
      "uuid": "51f85302-ef89-4d38-9135-8fd5dbbe9110",
      "form_id": "QCQ2jteXaiplqrKpNW_5nNFaKcwuMPwojCxUUbg_OeEbjbno8Aw8riPxO31TUUqbejHtf8l0h9upQJLmgOFHIg",
      "url": "/form/51f85302-ef89-4d38-9135-8fd5dbbe9110/QCQ2jteXaiplqrKpNW_5nNFaKcwuMPwojCxUUbg_OeEbjbno8Aw8riPxO31TUUqbejHtf8l0h9upQJLmgOFHIg/"
    }
  ]
}
```
 - `/api/form/<uuid>/<form_id>` Returns a single form's properties, including all of its fields. An example is shown below:
```json
$  curl https://cloak.theavid.dev/api/form/f3d43289-6844-4829-93ce-1cb4b4c3f6e1/3gCSZMsdjBfiEQGJnkKROIh2CsMWq24fHz9Sr0-wJsBjDBCc8Hp8rP78PLfLPkaoBMB9vQ6MyhTot6_mlY6egg/ | jq 

{
  "name": "Club Presidents Club Application",
  "description": "Thank you for displaying interest in joining the Club Presidents Club! Please fill out the form below to get a chance at one of the coveted executive spots. Don't worry, your personal details will be completely secret to any reviewers until, and only when, you have been accepted.",
  "fields": [
    {
      "question": "What grade are you in?",
      "description": "",
      "input_type": "N",
      "choices": [],
      "is_secret": false,
      "is_required": true
    },
    {
      "question": "What spot are you applying for?",
      "description": "",
      "input_type": "M",
      "choices": [
        "Executive",
        "Vice President",
        "President"
      ],
      "is_secret": false,
      "is_required": true
    },
    {
      "question": "What is your shirt size",
      "description": "We'd love to send you a shirt if you get accepted :D",
      "input_type": "S",
      "choices": [],
      "is_secret": true,
      "is_required": true
    },
    {
      "question": "Please explain why you'd like to be in this club:",
      "description": "",
      "input_type": "L",
      "choices": [],
      "is_secret": false,
      "is_required": true
    }
  ]
}```
