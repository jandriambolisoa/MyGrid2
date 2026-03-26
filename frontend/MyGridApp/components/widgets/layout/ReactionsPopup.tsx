import { Constants, GlobalStyles, Colors } from "@/theme";
import { BlurView } from "expo-blur";
import { StyleSheet, TouchableWithoutFeedback, View, Text, ScrollView, TouchableOpacity, Platform } from "react-native";
import { MainText } from "../ui/MainText";
import { ShadowButton } from "../buttons/ShadowButton";
import { useAuth } from "@/contexts/AuthContext";
import { useState } from "react";
import EmojiPicker from 'rn-emoji-keyboard';
import { useApi } from "@/hooks";
import { scopedI18n } from "@/translations/i18n";

export function ReactionsPopup ({
  reactions=[],
  setReactions,
  toggleReactions,
  userId=0,
  session=null,
} : {
  reactions?: any[];
  setReactions?: (datas: any) => void;
  toggleReactions?: () => void;
  userId?: number;
  session?: any;
}) {

  const t = scopedI18n('widgets.reactionsPopup');
  const auth = useAuth();

  const { loading, api: addReaction } = useApi();
  const { loading: delLoading, api: delReaction } = useApi(false, false);

  const [emojiOpen, setEmojiOpen] = useState(false);

  async function sendReaction(emoji: any) {
    const id = userId ? userId : auth.user.id
    const success = await addReaction({
      endpoint: `/events/sessions/predictions/reaction/${session.id}?user_id=${id}`,
      method: 'POST',
      body: { reaction: emoji.emoji },
      auth: auth
    })

    if (success) {
      setReactions?.([
        {
          reaction: emoji.emoji,
          user: { id: auth.user.id, username: auth.user.username }
        },
        ...reactions.filter((item) => item.user.id !== auth.user.id)
      ]);
    }
  }

  async function deleteReaction () {
    const id = userId ? userId : auth.user.id
    const success = await delReaction({
      endpoint: `/events/sessions/predictions/reaction/${session.id}?user_id=${id}`,
      method: 'DELETE',
      auth: auth
    })
    setReactions?.([
      ...reactions.filter((item) => item.user.id !== auth.user.id)
    ]);
  }

  function content () {

    if (!reactions.length) {
      return (
        <View style={{ alignSelf: 'stretch' }}>
          <MainText style={{ marginVertical: Constants.spacing.mainWidgetMargin }}>No reactions yet</MainText>
          <ShadowButton onPress={() => setEmojiOpen(true)}>
            <MainText>{t('addReaction')}</MainText>
          </ShadowButton>
        </View>
      )
    }

    function buttons () {
      if (reactions.find((item) => item.user.id === auth.user.id)) {
        return (
          <View style={{ alignSelf: 'stretch' }}>
            <ShadowButton style={{ marginTop: Constants.spacing.listMargin }} onPress={() => setEmojiOpen(true)}>
              <MainText>{t('modifyReaction')}</MainText>
            </ShadowButton>
            <ShadowButton style={{ marginTop: Constants.spacing.listMargin }} onPress={deleteReaction}>
              <MainText>{t('deleteReaction')}</MainText>
            </ShadowButton>
          </View>
        )
      }
      return (
        <ShadowButton style={{ marginTop: Constants.spacing.listMargin, alignSelf: 'stretch' }} onPress={() => setEmojiOpen(true)}>
          <MainText>{t('addReaction')}</MainText>
        </ShadowButton>
      )
    }

    return (
      <>
        <ScrollView style={{ alignSelf: 'stretch'}}>
          {reactions.map((item, index) => {
            return (
              <TouchableOpacity key={index} style={{ flexDirection: 'row', padding: Constants.spacing.listMargin }} activeOpacity={1}>
                <Text style={{ marginRight: Constants.spacing.listMargin }}>{item.reaction}</Text>
                <MainText>{item.user.username}</MainText>
              </TouchableOpacity>
            )
          })}
          </ScrollView>
        {buttons()}
      </>
    )
  }

  const backgroundColor = Platform.OS === 'ios' ? 'transparent' : '#c2c2c2cc'

  return (
    <>
      <TouchableWithoutFeedback onPress={toggleReactions}>
        <View style={[StyleSheet.absoluteFill, { alignItems: 'center', justifyContent: 'center' }]}>
          <TouchableWithoutFeedback>
            <BlurView tint='dark' intensity={20} style={[GlobalStyles.button, {
              width: '80%',
              maxHeight: '50%',
              justifyContent: 'flex-start',
              padding: Constants.spacing.buttonPadding,
              backgroundColor: backgroundColor
            }]}>
              <MainText bold={true} fontSize="header">{t('reactions')}</MainText>
              {content()}
            </BlurView>
          </TouchableWithoutFeedback>
        </View>
      </TouchableWithoutFeedback>
      <EmojiPicker onEmojiSelected={(e) => sendReaction(e)} open={emojiOpen} onClose={() => setEmojiOpen(false)}/>
    </>
  )
}