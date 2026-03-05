import { Header, ListsLabels, ResultsFooter, ResultsList, ScrollContainer } from "@/components/widgets";
import { useLocalSearchParams } from "expo-router";
import { View, ActivityIndicator, StyleSheet } from "react-native"
import { useEffect, useState } from "react"
import { useApi } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext";
import { niceDatetime } from "@/utils";
import { scopedI18n } from "@/translations/i18n";
import { Colors } from "@/theme";

export default function Results () {

  const auth = useAuth()
  const t = scopedI18n('sessions.results')

  const { id } = useLocalSearchParams();
  const { datas, error, loading, api: getResults } = useApi()

  const [headerHeight, setHeaderHeight] = useState(0);
  const [footerHeight, setFooterHeight] = useState(0);

  useEffect(() => {
    auth && getResults({
      endpoint: `/events/sessions/predictions/${id}`,
      method: 'GET',
      auth: auth
    })
  }, [auth])

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
      >
        
        <ListsLabels points={true} leftLabel={t('f1')}/>
      </Header>
      <ResultsFooter
        onLayout={(e: any) => setFooterHeight(e.nativeEvent.layout.height)}
        score={datas?.session.score}
        potentialScore={datas?.session.potential}
        spotColor={color2}
      />
      
    </View>
  )
}