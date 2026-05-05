<p align="center">
  <img src="https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=768,h=768,fit=crop/k1JwmslwXt9ap0c7/mygrid2_icon_transparent-2Ygt9rExd2tOp1GZ.png" width="200">
</p>

# MyGrid2 🏁

**MyGrid** is a motorsport prediction game built with a Python FastAPI backend and a React Native mobile app.

> **⚠️ Project in active development.**

![Copyright 2026 All rights reserved](https://img.shields.io/badge/©️%202026%20All%20rights%20reserved-8888bb)

[Website](https://mygrid-app.com/) | [Contact](mailto:contact@mygrid-app.com)

<br>

Alvailable on [iOS](https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg) and [Android](https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg)

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

- **Glass design**: Avant-garde art direction using transparency, svg gradients and blurs.
- **User-friendly**: Easy to use draggable list made with [react-native-reorderable-list](https://github.com/omahili/react-native-reorderable-list).
- **Architecture**: Highly modular, easy to modify and scalable.
- **State Management**: React Context for auth & toast messages.

## 💻 Manager Features

- **Manage everywhere**: Web dashboard for admins
- **Quick Management**: Easy to use draggable list made with [@dnd-kit](https://dndkit.com/).
- **Security First**: Cookies & backend interaction 100% server-side.

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

- ✅ Session records
  - See the 3 biggest user scores made over a single session
- ✅ Reactions
  - Add reactions over other users' predictions
  - Bubble-looking animation
- ✅ Manager
  - React web app
  - Add results, change registrations to events
  - Send notification to all users
- ⚙️ SSO Google & Apple
- ⚙️ Leagues
  - Invite friends with a link
  - Sorting system in the global leaderboard to display only members of one league

---

## Authors

- Backend Lead : [@jandriambolisoa](https://www.github.com/jandriambolisoa)
- Frontend Lead : [@theoduh](https://www.github.com/theoduh)

<!-- LINKS -->
[postgresql-badge]: https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white
[postgresql-link]: https://www.postgresql.org/
[reactnative-badge]: https://img.shields.io/badge/-React%20native-000?&logo=React
