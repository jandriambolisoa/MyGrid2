import * as Notifications from 'expo-notifications';
import * as Constants from 'expo-constants'

export async function getPushTokenAsync() {

  console.warn('Function getPushTokenAsync has been disabled')
  /*
  const { status } = await Notifications.getPermissionsAsync();
  if (status !== 'granted') {
    const { status: newStatus } = await Notifications.requestPermissionsAsync();
    if (newStatus !== 'granted') return null;
  }
  const tokenData = await Notifications.getExpoPushTokenAsync();
  return tokenData.data;
  */
}