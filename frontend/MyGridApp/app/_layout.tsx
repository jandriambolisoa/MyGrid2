import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';
import { useCallback } from 'react';
import { Stack } from 'expo-router';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { StyleSheet, View } from 'react-native';
import { MyGridBackground } from '@/components/widgets';
import { Colors } from '@/theme';
import { AuthProvider } from '@/contexts/AuthContext';

SplashScreen.preventAutoHideAsync();

export default function Layout() {

  const [fontsLoaded] = useFonts({
    AlteHaasGrotesk: require('../assets/fonts/AlteHaasGroteskRegular.ttf'),
    'AlteHaasGrotesk-Bold': require('../assets/fonts/AlteHaasGroteskBold.ttf'),
  });

  const onLayoutRootView = useCallback(async () => {
    if (fontsLoaded) {
      await SplashScreen.hideAsync();
    }
  }, [fontsLoaded]);

  if (!fontsLoaded) return null;

  return (
    <SafeAreaProvider onLayout={onLayoutRootView}>
      <AuthProvider>
        <View style={{ flex: 1, alignSelf: 'stretch', backgroundColor: Colors.light.background}}>
          <View style={StyleSheet.absoluteFill}>
            <MyGridBackground />
          </View>
          <Stack screenOptions={{ headerShown: false, contentStyle: { backgroundColor: 'transparent' } }}>
            <Stack.Screen name="index" />
          </Stack>
        </View>
      </AuthProvider>
    </SafeAreaProvider>
  );
}
