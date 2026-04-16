[forks-shield]: https://img.shields.io/github/forks/ItsMavey/SOEN357.svg?style=for-the-badge
[forks-url]: https://github.com/ItsMavey/SOEN357/network/members
[stars-shield]: https://img.shields.io/github/stars/ItsMavey/SOEN357.svg?style=for-the-badge
[stars-url]: https://github.com/ItsMavey/SOEN357/stargazers
[issues-shield]: https://img.shields.io/github/issues/ItsMavey/SOEN357.svg?style=for-the-badge
[issues-url]: https://github.com/ItsMavey/SOEN357/issues
[license-shield]: https://img.shields.io/badge/License-Proprietary-red.svg?style=for-the-badge
[license-url]: LICENSE.md

<!-- PROJECT LOGO -->
<div align="center">

[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Personal][license-shield]][license-url]

  <a href="https://github.com/ItsMavey/SOEN357">
    <img src="https://raw.githubusercontent.com/othneildrew/Best-README-Template/master/images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">SOEN357 - Project Submission</h3>

  <p align="center">
    Bing Chilling
    <br />
    <br />
    <a href="https://github.com/ItsMavey/SOEN357"><strong>Explore the docs »</strong></a>
    <br />
    <a href="https://github.com/ItsMavey/SOEN357/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/ItsMavey/SOEN357/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
    <br />
    <br />
  </p>

[![Email](https://img.shields.io/badge/contact%40itsmavey.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:contact@itsmavey.com)
[![GitHub](https://img.shields.io/badge/ItsMavey-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ItsMavey)

</div>

***

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#team-members">Team Members</a></li>
    <li><a href="#local-development">Local Development</a></li>
    <li><a href="#tech-stack">Tech Stack</a></li>
    <li><a href="#contributors">Contributors</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

***

## About The Project

This is the submission of the Term Project for the course SOEN 357, given by Hakim Mellah at Concordia University.

***

## Team Members

| Name        | Student ID |
|:------------|:-----------|
| Adam Ousmer | `40246695` |
| Yayi Chen  | `40286042` |

***

## Local Development

You can run the project locally using either Docker Compose (recommended) or a direct Python virtual environment.

### Prerequisites

* [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/) OR
* [Python 3.10+](https://www.python.org/downloads/)

### Option A: Using Docker Compose (Recommended)

1. Clone the repository and navigate into the project directory:
   ```sh
   git clone https://github.com/ItsMavey/SOEN357.git
   cd SOEN357
   ```
2. Build and start the containers using docker-compose:
   ```sh
   docker-compose up --build
   ```
3. The application will be accessible at:
   [http://localhost:8000](http://localhost:8000)

### Option B: Using Python Virtual Environment

1. Clone the repository and navigate into the project directory:
   ```sh
   git clone https://github.com/ItsMavey/SOEN357.git
   cd SOEN357
   ```
2. Create and activate a Python virtual environment:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirement.txt
   ```
4. Apply the database migrations:
   ```sh
   python manage.py migrate
   ```
5. Start the local development server:
   ```sh
   python manage.py runserver
   ```
6. The application will be accessible at:
   [http://localhost:8000](http://localhost:8000)

***

### Tech Stack

#### Languages

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

#### Technologies & Tools

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%23499848.svg?style=for-the-badge&logo=gunicorn&logoColor=white)

#### DevOps

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)

***

## Contributors

This project exists thanks to the people who contribute.

<a href="https://github.com/ItsMavey/SOEN357/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ItsMavey/SOEN357" />
</a>

***

## Contributing

If you have suggestions for how this project could be improved, or want to report a bug, please open an issue! We'd love to hear your ideas and help you fix any problems.

For contributing code, please contact us directly before making any changes or submitting a pull request.

***

## License

This project is licensed under the Proprietary License Agreement - see the [LICENSE](LICENSE.md) file for details.

***

## Contact

ItsMavey - [GitHub](https://github.com/ItsMavey) - [Email](mailto:contact@itsmavey.com)

***

## Acknowledgements

README template inspired by [othneildrew/Best-README-Template](https://github.com/othneildrew/Best-README-Template)
