import { ExpoConfig } from "expo/config";

const config: ExpoConfig = {
  name: "MyGridApp",
  slug: "MyGridApp",
  version: "2.1.1",
  orientation: "portrait",
  icon: "./assets/images/app/mygrid2_icon_v001.png",
  scheme: "mygridapp",
  userInterfaceStyle: "automatic",
  newArchEnabled: true,

  ios: {
    supportsTablet: true,
    usesAppleSignIn: true,
    bundleIdentifier: "com.theoduh.mygridapp",
    config: {
      usesNonExemptEncryption: false,
    },
  },

  android: {
    icon: "./assets/images/app/mygrid2_icon_v001.png",
    adaptiveIcon: {
      foregroundImage: "./assets/images/app/mygrid2_adaptive-icon-foreground.png",
      backgroundImage: "./assets/images/app/mygrid2_adaptive-icon-background.png",
      backgroundColor: "#ffffff"
    },
    edgeToEdgeEnabled: true,
    package: "com.theoduh.mygridapp",
    blockedPermissions: [
      "android.permission.ACTIVITY_RECOGNITION"
    ],
    googleServicesFile: process.env.GOOGLE_SERVICES_JSON,
  },

  web: {
    bundler: "metro",
    output: "static",
    favicon: "./assets/images/favicon.png",
  },

  plugins: [
    "expo-router",
    [
      "expo-splash-screen",
      {
        image: "./assets/images/app/mygrid2_splash.png",
        imageWidth: 200,
        resizeMode: "contain",
        backgroundColor: "#dddddd",
      },
    ],
    [
      "expo-font",
      {
        fonts: [
          "./assets/fonts/AlteHaasGroteskRegular.ttf",
          "./assets/fonts/AlteHaasGroteskBold.ttf",
        ],
      },
    ],
    [
      "expo-image-picker",
      {
        photosPermission: "The app needs access to your photos.",
        colors: {
          cropToolbarColor: "#000000",
        },
        dark: {
          colors: {
            cropToolbarColor: "#000000",
          },
        },
      },
    ],
    [
      "expo-navigation-bar",
      {
        enforceContrast: true,
        barStyle: "light",
        visibility: "hidden",
      }
    ],
    "expo-localization",
    "expo-apple-authentication",
    "expo-secure-store",
    "expo-web-browser",
  ],

  experiments: {
    typedRoutes: true,
  },

  extra: {
    router: {},
    eas: {
      projectId: "72487323-920f-438f-852a-aee635a98f43",
    },
  },

  owner: "theoduh",
};

export default config;