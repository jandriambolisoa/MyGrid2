import { useAuth } from "@/contexts/AuthContext";
import { scopedI18n } from "@/translations/i18n";
import { useLocalSearchParams } from "expo-router";
import { useEffect, useState } from "react";
import { useApi } from "@/hooks";
import { View, StyleSheet, ActivityIndicator } from "react-native";
import { ResultsList, ScrollContainer, Header, ResultsFooter, ListsLabels } from "@/components/widgets";
import { Colors } from "@/theme";
import { niceDatetime } from "@/utils";


export default function UserResults () {
  const auth = useAuth();
  const t = scopedI18n('sessions.results')

  const { userId, sessionId } = useLocalSearchParams();
  const { datas, error, loading, api: getResults } = useApi(true);

  const [headerHeight, setHeaderHeight] = useState(0);
  const [footerHeight, setFooterHeight] = useState(0);

  useEffect(() => {
    auth && getResults({
      endpoint: `/events/sessions/predictions/${sessionId}?user_id=${userId}`,
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