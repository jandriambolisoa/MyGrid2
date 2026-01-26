import { Container } from '@/components/widgets/Container';
import { TouchableOpacity, View, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';
import { MainText } from '@/components/widgets/MainText';
import { SpotLight } from '@/components/widgets/SpotLight';

export default function MainScreen () {

  const router = useRouter();

  return (
    <Container style={{ justifyContent: 'center', alignItems: 'center' }}>
      <View style={[StyleSheet.absoluteFill]}>
        <SpotLight color="#ff7300" cx="90%" cy="20%" fx="90%" fy="20%" radius="60%"/>
        <SpotLight color="#00fff0" cx="10%" cy="80%" fx="10%" fy="80%" radius="60%"/>
      </View>
      <View style={{alignItems: 'center', justifyContent: 'center', position: 'absolute', top: "45%"}}>
        <MainText style={[{fontSize: 16}]}>Welcome to</MainText>
        <MainText style={{fontSize: 64, marginBottom: 40}}>Mygrid</MainText>
      </View>
      <TouchableOpacity onPress={() => router.push('/auth/login')} style={[{borderWidth: 1, borderColor: 'white', padding: 10, borderRadius: 4, position: 'absolute', bottom: "30%"}]}>
        <MainText>Sign in</MainText>
      </TouchableOpacity>
    </Container>
  )
}

const styles = StyleSheet.create({
  absolute: {
    position: "absolute",
    alignSelf: "center"
  }
})