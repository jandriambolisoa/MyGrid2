import { View } from 'react-native';
import { useRouter } from 'expo-router';
import { Container, MainText, LiteButton } from '@/components/widgets';
import { Constants } from '@/theme';

export default function MainScreen () {

  const router = useRouter();

  return (
    <Container style={{ backgroundColor: 'transparent'}}>
      
      <View style={{alignItems: 'center', justifyContent: 'center', position: 'absolute', top: "45%"}}>
        <MainText>Welcome to</MainText>
        <MainText style={{fontSize: Constants.fontSizes.giant, marginBottom: 40}}>Mygrid</MainText>
      </View>
      <LiteButton onPress={() => router.push('/auth/login')} style={[{position: 'absolute', bottom: "30%"}]}>
        <MainText>Sign in</MainText>
      </LiteButton>
    </Container>
  )
}