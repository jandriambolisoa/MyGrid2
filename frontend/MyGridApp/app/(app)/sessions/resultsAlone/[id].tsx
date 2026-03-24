import { ScrollContainer, Header, ResultsAlonelist, ListsLabels } from "@/components/widgets";
import { useAuth } from "@/contexts/AuthContext";
import { useLocalSearchParams } from "expo-router";
import { useState, useEffect } from "react";
import { View, ActivityIndicator, StyleSheet } from "react-native";
import { useApi } from "@/hooks"
import { niceDatetime } from "@/utils";
import { scopedI18n } from "@/translations/i18n";
import { Colors } from "@/theme";
import { useToast } from "@/contexts/ToastContext";
import * as SecureStore from "expo-secure-store";

export default function ResultsAlone () {

  const auth = useAuth();
  const t = scopedI18n('sessions.results');

  const { id } = useLocalSearchParams();
  const { datas, loading, api: getResults } = useApi(true);
  const { showToast } = useToast();

  const [headerHeight, setHeaderHeight] = useState(0);

  useEffect(() => {
    auth && getResults({
      endpoint: `/events/sessions/results/${id}`,
      auth: auth
    })
  }, [auth])

  const color1 = datas?.session.event_colors[0]

  async function handleCopy () {
    if (datas?.results.length) {
      await SecureStore.setItemAsync('clipboard', JSON.stringify(datas.results.map((item: any) => item.driver.id)));
      showToast({
        title: t('resultsCopied'),
        duration: 2500
      })
    }
  }

  return (
    <View style={{ flex: 1 }}>
      {loading && <View style={[StyleSheet.absoluteFill, { justifyContent: 'center', alignItems: 'center', backgroundColor: Colors.light.background }]}>
        <ActivityIndicator color={Colors.light.orangeLogo}/>
      </View>}
      {datas && <ScrollContainer headerHeight={headerHeight}>
        <ResultsAlonelist datas={datas.results}/>
      </ScrollContainer>}

      <Header
        onLayout={(e: any) => setHeaderHeight(e.nativeEvent.layout.height)}
        title={datas?.session.name ? datas.session.name : t('loading')}
        subtitle={datas?.session?.datetime && niceDatetime(datas.session.datetime, false)}
        spotColor={color1}
        menu={[
          {
            title: t('copyResults'),
            onPress: handleCopy
          }
        ]}
      >
        <ListsLabels noGrid={true}/>
      </Header>
    </View>
  )
}