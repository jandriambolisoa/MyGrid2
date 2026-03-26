import { useAuth } from "@/contexts/AuthContext";
import { scopedI18n } from "@/translations/i18n";
import { useLocalSearchParams } from "expo-router";
import { useEffect, useState } from "react";
import { useApi } from "@/hooks";
import { View, StyleSheet, ActivityIndicator } from "react-native";
import { ResultsList, ScrollContainer, Header, ResultsFooter, ListsLabels, ReactionsPopup } from "@/components/widgets";
import { Colors } from "@/theme";
import { userScore } from "@/utils";
import { useToast } from "@/contexts/ToastContext";
import * as SecureStore from "expo-secure-store";

export default function UserResults () {
  const auth = useAuth();
  const t = scopedI18n('rankings');

  const { userId, sessionId } = useLocalSearchParams();
  const { datas, loading, api: getResults } = useApi(true);
  const { showToast } = useToast();

  const [headerHeight, setHeaderHeight] = useState(0);
  const [footerHeight, setFooterHeight] = useState(0);
  const [showReactions, setShowReactions] = useState(false);

  const [reactions, setReactions] = useState([]);

  useEffect(() => {
    auth && getResults({
      endpoint: `/events/sessions/predictions/${sessionId}?user_id=${userId}`,
      auth: auth
    })
  }, [auth])

  useEffect(() => {
    if (datas?.session?.reactions) {
      setReactions(datas.session.reactions);
    }
  }, [datas])

  async function handleCopy () {
    if (datas?.predictions.length) {
      await SecureStore.setItemAsync('clipboard', JSON.stringify(datas.predictions.map((item: any) => item.driver.id)));
      showToast({
        title: t('predictionCopied'),
        duration: 2500
      })
    }
  }

  function handleShowReactions () {
    setShowReactions(!showReactions);
  }

  const color1 = datas?.session.event_colors[0]
  const color2 = datas?.session.event_colors.length > 1 ? datas?.session.event_colors[1] : color1

  return (
    <View style={{ flex: 1, }}>
      {loading && <View style={[StyleSheet.absoluteFill, { justifyContent: 'center', alignItems: 'center', backgroundColor: Colors.light.background }]}>
        <ActivityIndicator color={Colors.light.orangeLogo}/>
      </View>}
      {datas && <ScrollContainer headerHeight={headerHeight} footerHeight={footerHeight}>
        <ResultsList datas={datas.predictions}/>
      </ScrollContainer>}

      <Header
        onLayout={(e: any) => setHeaderHeight(e.nativeEvent.layout.height)}
        title={datas?.session.name ? datas.session.name : t('loading')}
        subtitle={userScore(datas?.user?.username ?? '')}
        spotColor={color1}
        menu={[
          {
            title: t('copyPrediction'),
            onPress: handleCopy
          }
        ]}
      >
        
        <ListsLabels points={true} leftLabel={t('f1')} self={true}/>
      </Header>
      <ResultsFooter
        onLayout={(e: any) => setFooterHeight(e.nativeEvent.layout.height)}
        score={datas?.session.score}
        potentialScore={datas?.session.potential}
        spotColor={color2}
        reactions={reactions}
        toggleReactions={handleShowReactions}
      />
      {showReactions && <ReactionsPopup toggleReactions={handleShowReactions} reactions={reactions} setReactions={setReactions}/>}
    </View>
  )
}