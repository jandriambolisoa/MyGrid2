import { GlobalStyles, Constants } from "@/theme";
import { View, ViewProps, StyleSheet, Image, FlatList } from "react-native";
import { ShadowSetup, MainText, SpotLight, LiteButton } from "@/components/widgets";

export function MainWidget({ style, ...otherProps }: ViewProps) {

  const data = {
    sessions: [
      {
        name: "Practice 1"
      },
      {
        name: "Sprint Qualifying"
      },
      {
        name: "Sprint Race"
      },
      {
        name: "Qualifying"
      },
      {
        name: "Feature Race"
      }
    ]
  }

  function renderItem({item} : any) {

    return(
      <LiteButton style={{ alignSelf: "stretch", marginBottom: Constants.spacing.buttonPadding }}>
        <MainText>{item.name}</MainText>
      </LiteButton>
    )
  }

  return (
    <View style={[GlobalStyles.button, GlobalStyles.mainWidget, style]} {...otherProps}>
      <SpotLight color="#ef333f" cx="35%" cy="35%" fx="5%" fy="5%" radius="50%"/>
      <SpotLight color="#fdda25" cx="70%" cy="70%" fx="95%" fy="95%" radius="45%"/>
      <ShadowSetup />
      <View style={[StyleSheet.absoluteFill, { padding: Constants.spacing.buttonPadding , alignItems: 'center' }]}>
        <MainText style={{ fontSize: 28, marginTop: 20 }}>Belgium</MainText>
        <Image resizeMode="stretch" style={{ position: 'absolute', width: 50, height: 50, top: 20, right: "10%" }} source={require('@/assets/images/demo/spa.png')}/>
        <Image resizeMode="contain" style={{ height: "30%", marginVertical: 30 }} source={require('@/assets/images/demo/trophy_belgium.png')}/>
        <FlatList
          data={data.sessions}
          renderItem={renderItem}
          scrollEnabled={false}
          style={{ alignSelf: "stretch" }}
        />
      </View>
    </View>
  )
}