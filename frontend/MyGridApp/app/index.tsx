import { StyleSheet, View } from "react-native";
import { BlurView } from "expo-blur";

export default function MainScreen () {
  return (
    <View style={styles.container}>
        <View style={{ marginHorizontal: 20, marginVertical: 60, flex: 1, overflow: 'hidden'}}>
          <View style={{ borderRadius: 200, backgroundColor: 'yellow', position: 'absolute', height: 200, width: 200, top: '50%', right: '60%'}}/>
          <View style={{ borderRadius: 200, backgroundColor: 'black', position: 'absolute', height: 200, width: 200, top: '20%', right: '30%'}}/>
          <View style={{ borderRadius: 200, backgroundColor: 'red', position: 'absolute', height: 200, width: 200, top: '60%', right: '45%'}}/>
          <BlurView intensity={200} style={styles.widget} tint='light'>

          </BlurView>
          
        </View>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#dddddd"
  },
  widget: {
    borderColor: "white",
    borderWidth: 0.5,
    borderRadius: 4,
    height: "100%",
    width: "100%"
  }
})