# MyGrid2 🏁

**MyGrid** is a motorsport prediction game built with a Python FastAPI backend and a React Native mobile app.

> **⚠️ Project in active development.**

![Copyright 2026 All rights reserved](https://img.shields.io/badge/©️%202026%20All%20rights%20reserved-8888bb)

[Website](https://mygrid-app.com/) | [Contact](mailto:contact@mygrid-app.com)

<br>
<a href="https://play.google.com/store/apps/details?id=com.theoduh.mygridapp">
  <img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg" width="110">
</a>&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://apps.apple.com/us/app/mygrid/id6739147623">
  <img src="https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg" width="100">
</a>

## 🏗️ Project Structure

This is a monorepo containing both the logic and the interface:
*   **/backend**: FastAPI, PostgreSQL, and Poetry.
*   **/frontend**: React Native mobile app made with Expo.
*   **/manager**: React web dashboard for moderation made with Next.js.

---

## ⚙️ Backend Features

- **User Management**: Profile creation, SSO integration, and moderation tools.
- **Micro-services Architecture**: Multiple FastAPI instances for workload optimization.
- **Containerized**: Fully Dockerized for seamless deployment via `docker-compose`.
- **Security First**: Implementation of JWT tokens and Argon2 hashing.
- **Bulletproof Code**: Unit tests via Pytest (Targeting 100% endpoint coverage).

## 📱 Frontend Features

- **Design**: Experimental glass visuals using transparency, svg gradients and blurs.
- **User-friendly**: Easy to use draggable list made with react-native-reorderable-list.
- **Architecture**: Highly modular, easy to modify and scalable.
- **Development speed**: Fast pipeline with Expo.
- **State Management**: React Context for auth & toast messages.

## 💻 Manager Features

- **Quick Management**: Easy to use draggable list made with [@dnd-kit](https://dndkit.com/).
- **Security**: Cookies & backend interaction 100% server-side.
- **Development speed**: Fast pipeline with Next.js.

---

## 🛠️ Tech Stack

| Component | Technology                                                                                                                                    |
| :--- |:----------------------------------------------------------------------------------------------------------------------------------------------|
| **Database** | [PostgreSQL][postgresql-link]                                                                                                     |
| **Migrations** | [Dbmate](https://github.com/amacneil/dbmate)                                                                                                  |
| **Package Manager** | [Poetry](https://python-poetry.org/), [NPM](https://www.npmjs.com/)       |
| **Frameworks** | [FastAPI](https://fastapi.tiangolo.com/), [React Native](https://reactnative.dev/), [Expo](https://expo.dev/), [React](https://fr.react.dev/), [Next.js](https://nextjs.org/) |

---

## 📍 Roadmap

- [x] Session records
- [x] Reactions
- [x] Manager
- [ ] oAuth Google & Apple
- [ ] Leagues

---

## Authors

- Backend Lead : [@jandriambolisoa](https://www.github.com/jandriambolisoa)
- Frontend Lead : [@theoduh](https://www.github.com/theoduh)

<!-- LINKS -->
[postgresql-badge]: https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white
[postgresql-link]: https://www.postgresql.org/
[reactnative-badge]: https://img.shields.io/badge/-React%20native-000?&logo=React
