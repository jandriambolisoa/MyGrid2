import { Container } from '@/components/widgets/Container';
import { MainText } from '@/components/widgets/MainText';
import { MainWidget } from '@/components/widgets/MainWidget';
import { StyleSheet, View } from 'react-native';

export default function MainScreen () {

  return (
    <Container>
      <MainWidget>
        <MainText type="light">
          Welcome to MyGridApp!</MainText>
      </MainWidget>
    </Container>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#dddddd"
  }
})