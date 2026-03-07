import { ScrollContainer, Header, ResultsAlonelist, ListsLabels } from "@/components/widgets";
import { useAuth } from "@/contexts/AuthContext";
import { useLocalSearchParams } from "expo-router";
import { useState, useEffect } from "react";
import { View, ActivityIndicator, StyleSheet } from "react-native";
import { useApi } from "@/hooks"
import { niceDatetime } from "@/utils";
import { scopedI18n } from "@/translations/i18n";
import { Colors } from "@/theme";

export default function ResultsAlone () {

  const auth = useAuth()
  const t = scopedI18n('sessions.results')

  const { id } = useLocalSearchParams();
  const { datas, error, loading, api: getResults } = useApi(true)

  const [headerHeight, setHeaderHeight] = useState(0);
  const [footerHeight, setFooterHeight] = useState(0);

  useEffect(() => {
    auth && getResults({
      endpoint: `/events/sessions/results/${id}`,
      auth: auth
    })
  }, [auth])

  const color1 = datas?.session.event_colors[0]

  return (
    <View style={{ flex: 1 }}>
      {loading && <View style={[StyleSheet.absoluteFill, { justifyContent: 'center', alignItems: 'center', backgroundColor: Colors.light.background }]}>
        <ActivityIndicator color={Colors.light.orangeLogo}/>
      </View>}
      {datas && <ScrollContainer headerHeight={headerHeight} footerHeight={footerHeight}>
        <ResultsAlonelist datas={datas.results}/>
      </ScrollContainer>}

      <Header
        onLayout={(e: any) => setHeaderHeight(e.nativeEvent.layout.height)}
        title={datas?.session.name ? datas.session.name : t('loading')}
        subtitle={datas?.session?.datetime && niceDatetime(datas.session.datetime, false)}
        spotColor={color1}
      >
        <ListsLabels noGrid={true}/>
      </Header>
    </View>
  )
}