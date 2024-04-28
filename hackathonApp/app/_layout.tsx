import { useFonts } from "expo-font";
import { Link, Stack } from "expo-router";
import * as SplashScreen from "expo-splash-screen";
import React, { useEffect } from "react";
import { Pressable, Text } from "react-native";
import { Ionicons } from "@expo/vector-icons";

export {
  // Catch any errors thrown by the Layout component.
  ErrorBoundary,
} from "expo-router";

export const unstable_settings = {
  // Ensure that reloading on `/modal` keeps a back button present.
  initialRouteName: "(tabs)",
};

// Prevent the splash screen from auto-hiding before asset loading is complete.
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const [loaded, error] = useFonts({
    NiveauGrotesk: require("../assets/fonts/NiveauGroteskRegular.otf"),
    "niv-b": require("../assets/fonts/NiveauGroteskBold.otf"),
    "niv-l": require("../assets/fonts/NiveauGroteskLight.otf"),
    "niv-li": require("../assets/fonts/NiveauGroteskLight-Italic.otf"),
    "niv-m": require("../assets/fonts/NiveauGroteskMedium.otf"),
    "niv-r-smallcaps": require("../assets/fonts/NiveauGroteskRegular-SmallCaps.otf"),
  });

  // Expo Router uses Error Boundaries to catch errors in the navigation tree.
  useEffect(() => {
    if (error) throw error;
  }, [error]);

  useEffect(() => {
    if (loaded) {
      SplashScreen.hideAsync();
    }
  }, [loaded]);

  if (!loaded) {
    return null;
  }

  return <RootLayoutNav />;
}

function RootLayoutNav() {
  return (
    <Stack
      screenOptions={{
        headerShown: true,
      }}
    >
      <Stack.Screen name="index" options={{ headerShown: false }} />
      <Stack.Screen name="result/index" options={{ headerShown: false }} />
      <Stack.Screen
        name="insert-text"
        options={{
          headerTitle: () => {
            return <Text style={{ fontSize: 20 }}>Let's start</Text>;
          },
          headerLeft: () => {
            return (
              <Link href={"/"} asChild>
                <Pressable>
                  <Ionicons name="arrow-back" size={24} color="black" />
                </Pressable>
              </Link>
            );
          },
        }}
      />
      <Stack.Screen
        name="insert-pic"
        options={{
          headerTitle: () => {
            return <Text style={{ fontSize: 20 }}>Upload file</Text>;
          },
          headerLeft: () => {
            return (
              <Link href={"/"} asChild>
                <Pressable>
                  <Ionicons name="arrow-back" size={24} color="black" />
                </Pressable>
              </Link>
            );
          },
        }}
      />
    </Stack>
  );
}
