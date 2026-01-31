import { withLayoutContext } from 'expo-router';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { MainTabBar } from '@/components/widgets/MainTabBar';

const Tab = createBottomTabNavigator();
const ExpoRouterTabs = withLayoutContext(Tab.Navigator);

export default function TabLayout() {

  return (
    <ExpoRouterTabs
      screenOptions={{ headerShown: false, animation: 'shift' }}
      tabBar={(props) => <MainTabBar {...props} />}
    >
      <ExpoRouterTabs.Screen name="social" options={{ title: "Social" }} />
      <ExpoRouterTabs.Screen name="index" options={{ title: "Home" }} />
      <ExpoRouterTabs.Screen name="profile" options={{ title: "Profile" }} />
    </ExpoRouterTabs>
  );
}