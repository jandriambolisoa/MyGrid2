# MyGrid2 🏁

**MyGrid** is a motorsport prediction game built with a Python FastAPI backend and a React Native / React mobile app.

> **⚠️ Project in active development.**

[![Copyright](https://img.shields.io/badge/©️%202026%20All%20rights%20reserved-8888bb)](https://choosealicense.com/licenses/mit/)

[Website](https://mygrid-app.com/) | [Contact](mailto:contact@mygrid-app.com)
## 🏗️ Project Structure

This is a monorepo containing both the logic and the interface:
*   **/backend**: FastAPI, PostgreSQL, and Poetry.
*   **/frontend**: React Native mobile app
*   **/manager**: React web dashboard for moderation

---

## ⚙️ Backend Features

- **User Management**: Profile creation, SSO integration, and moderation tools.
- **Micro-services Architecture**: Multiple FastAPI instances for workload optimization.
- **Containerized**: Fully Dockerized for seamless deployment via `docker-compose`.
- **Security First**: Implementation of JWT tokens and Argon2 hashing.
- **Bulletproof Code**: Unit tests via Pytest (Targeting 100% endpoint coverage).

## 📱 Frontend Features

- **TODO**: TODO

---

## 🛠️ Tech Stack

| Component | Technology                                                                                                                                    |
| :--- |:----------------------------------------------------------------------------------------------------------------------------------------------|
| **Database** | [PostgreSQL](https://www.postgresql.org/)                                                                                                     |
| **Migrations** | [Dbmate](https://github.com/amacneil/dbmate)                                                                                                  |
| **Package Manager** | [Poetry](https://python-poetry.org/)                                                                                                          |
| **Frameworks** | [FastAPI](https://fastapi.tiangolo.com/), [React Native](https://reactnative.dev/), [Expo](https://expo.dev/), [React](https://fr.react.dev/) |

---

## Authors

- Backend Lead : [@jandriambolisoa](https://www.github.com/jandriambolisoa)
- Frontend Lead : [@theoduh](https://www.github.com/theoduh)