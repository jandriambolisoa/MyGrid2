import { View, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';
import { Container, MainText, SpotLight, LiteButton } from '@/components/widgets';
import { Colors } from '@/theme';

export default function MainScreen () {

  const router = useRouter();

  return (
    <Container>
      <View style={[StyleSheet.absoluteFill]}>
        <SpotLight color={Colors.light.orangeLogo} cx="90%" cy="20%" fx="90%" fy="20%" radius="60%"/>
        <SpotLight color={Colors.light.cyanLogo} cx="10%" cy="80%" fx="10%" fy="80%" radius="60%"/>
      </View>
      <View style={{alignItems: 'center', justifyContent: 'center', position: 'absolute', top: "45%"}}>
        <MainText style={[{fontSize: 16}]}>Welcome to</MainText>
        <MainText style={{fontSize: 64, marginBottom: 40}}>Mygrid</MainText>
      </View>
      <LiteButton onPress={() => router.push('/home')} style={[{position: 'absolute', bottom: "30%"}]}>
        <MainText>Sign in</MainText>
      </LiteButton>
    </Container>
  )
}