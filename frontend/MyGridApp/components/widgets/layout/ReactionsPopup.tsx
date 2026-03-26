import { Constants, GlobalStyles } from "@/theme";
import { BlurView } from "expo-blur";
import { StyleSheet, TouchableWithoutFeedback, View, Text } from "react-native";
import { MainText } from "../ui/MainText";
import { ShadowButton } from "../buttons/ShadowButton";
import { useAuth } from "@/contexts/AuthContext";

export function ReactionsPopup ({
  reactions=[],
  setReactions,
  toggleReactions,
} : {
  reactions?: any[];
  setReactions?: (datas: any) => void;
  toggleReactions?: () => void;
}) {

  const { user } = useAuth();

  function content () {

    if (!reactions.length) {
      return (
        <View>
          <MainText style={{ marginVertical: Constants.spacing.mainWidgetMargin }}>No reactions yet</MainText>
          <ShadowButton>
            <MainText>Add reaction</MainText>
          </ShadowButton>
        </View>
      )
    }

    function buttons () {
      if (reactions.find((item) => item.user.id === user.id)) {
        return (
          <View>
            <ShadowButton style={{ marginTop: Constants.spacing.listMargin }}>
              <MainText>Modify reaction</MainText>
            </ShadowButton>
            <ShadowButton style={{ marginTop: Constants.spacing.listMargin }}>
              <MainText>Delete reaction</MainText>
            </ShadowButton>
          </View>
        )
      }
      return (
        <ShadowButton style={{ marginTop: Constants.spacing.listMargin }}>
          <MainText>Add reaction</MainText>
        </ShadowButton>
      )
    }

    return (
      <View style={{ alignSelf: 'stretch' }}>
        {reactions.map((item, index) => {
          return (
            <View key={index} style={{ flexDirection: 'row', padding: Constants.spacing.listMargin }}>
              <Text style={{ marginRight: Constants.spacing.listMargin }}>{item.reaction}</Text>
              <MainText>{item.user.username}</MainText>
            </View>
          )
        })}
        {buttons()}
      </View>
    )
  }

  return (
    <TouchableWithoutFeedback onPress={toggleReactions}>
      <View style={[StyleSheet.absoluteFill, { alignItems: 'center', justifyContent: 'center' }]}>
        <TouchableWithoutFeedback>
          <BlurView tint='dark' intensity={20} style={[GlobalStyles.button, { width: '80%', maxHeight: '60%', justifyContent: 'flex-start', padding: Constants.spacing.buttonPadding }]}>
            <MainText bold={true} fontSize="header">Reactions</MainText>
            {content()}
          </BlurView>
        </TouchableWithoutFeedback>
      </View>
    </TouchableWithoutFeedback>
  )
}