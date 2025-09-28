import { Container } from '@/components/widgets/Container';
import { TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { MainText } from '@/components/widgets/MainText';

export default function MainScreen () {

  const router = useRouter();

  return (
    <Container style={{ justifyContent: 'center', alignItems: 'center' }}>
      <TouchableOpacity onPress={() => router.push('/auth/login')} style={{borderWidth: 1, borderColor: 'white', padding: 10, borderRadius: 4}}>
        <MainText>Sign in</MainText>
      </TouchableOpacity>
    </Container>
  )
}