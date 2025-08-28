import { Container } from '@/components/widgets/Container';
import { MainText } from '@/components/widgets/MainText';
import { MainWidget } from '@/components/widgets/MainWidget';
import { StyleSheet, View } from 'react-native';

export default function MainScreen () {

  return (
    <Container>
      <MainWidget borders={true} colors={["#ff6600", "#ff6600"]} style={{ alignItems: 'center', justifyContent: 'center' }}>
        <MainText type="light" style={{ }}>Welcome to MyGridApp!</MainText>
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