import * as Notifications from 'expo-notifications';

export async function getPushTokenAsync() {

  const { status } = await Notifications.getPermissionsAsync();

  if (status !== 'granted') {
    const { status: newStatus } = await Notifications.requestPermissionsAsync();
    if (newStatus !== 'granted') return null;
  }

  const tokenData = await Notifications.getExpoPushTokenAsync();

  return tokenData.data;
}