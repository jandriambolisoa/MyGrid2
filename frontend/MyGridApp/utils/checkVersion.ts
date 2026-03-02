import Constants from 'expo-constants';

export function checkVersion (myGridVersion: string): boolean {

  const localVersion = Constants.expoConfig?.version;

  if (!localVersion) return false;

  const [localMajor, localMinor] = localVersion.split('.').map(Number);
  const [remoteMajor, remoteMinor] = myGridVersion.split('.').map(Number);

  if (
    isNaN(localMajor) ||
    isNaN(localMinor) ||
    isNaN(remoteMajor) ||
    isNaN(remoteMinor)
  ) {
    return false;
  }

  if (remoteMajor < localMajor) return true
  if (remoteMajor > localMajor) return false

  return localMinor >= remoteMinor;
}