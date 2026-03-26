import { Header, ListsLabels, ResultsFooter, ResultsList, ScrollContainer } from "@/components/widgets";
import { useLocalSearchParams } from "expo-router";
import { View, ActivityIndicator, StyleSheet } from "react-native"
import { useEffect, useState } from "react"
import { useApi } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext";
import { niceDatetime } from "@/utils";
import { scopedI18n } from "@/translations/i18n";
import { Colors } from "@/theme";
import { useToast } from "@/contexts/ToastContext";
import * as SecureStore from "expo-secure-store";

export default function Results () {

  const auth = useAuth()
  const t = scopedI18n('sessions.results')

  const { id } = useLocalSearchParams();
  const { datas, loading, api: getResults } = useApi(true);
  const { showToast } = useToast();

  const [headerHeight, setHeaderHeight] = useState(0);
  const [footerHeight, setFooterHeight] = useState(0);

  useEffect(() => {
    auth && getResults({
      endpoint: `/events/sessions/predictions/${id}`,
      auth: auth
    })
  }, [auth])

  async function handleCopyPredictions () {
    if (datas?.predictions.length) {
      await SecureStore.setItemAsync('clipboard', JSON.stringify(datas.predictions.map((item: any) => item.driver.id)));
      showToast({
        title: t('predictionCopied'),
        duration: 2500
      })
    }
  }

  async function handleCopyResults () {
    if (datas?.predictions.length) {
      await SecureStore.setItemAsync('clipboard', JSON.stringify([...datas.predictions].sort((a: any, b: any) => {
        return a.result - b.result
      }).map((item: any) => item.driver.id)));
      showToast({
        title: t('resultsCopied'),
        duration: 2500
      })
    }
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
        subtitle={datas?.session?.datetime && niceDatetime(datas.session.datetime, false)}
        spotColor={color1}
        menu={[
          {
            title: t('copyPrediction'),
            onPress: handleCopyPredictions
          },
          {
            title: t('copyResults'),
            onPress: handleCopyResults
          }
        ]}
      >
        
        <ListsLabels points={true} leftLabel={t('f1')}/>
      </Header>
      <ResultsFooter
        onLayout={(e: any) => setFooterHeight(e.nativeEvent.layout.height)}
        score={datas?.session.score}
        potentialScore={datas?.session.potential}
        spotColor={color2}
        reactions={datas?.session?.reactions}
      />
      
    </View>
  )
}