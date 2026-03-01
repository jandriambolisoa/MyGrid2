import { ScrollContainer, Header, ResultsAlonelist, ListsLabels } from "@/components/widgets";
import { useAuth } from "@/contexts/AuthContext";
import { useLocalSearchParams } from "expo-router";
import { useState, useEffect } from "react";
import { View } from "react-native";
import { useApi } from "@/hooks"
import { niceDatetime } from "@/utils";

export default function ResultsAlone () {

  const auth = useAuth()

  const { id } = useLocalSearchParams();
  const { datas, error, loading, api: getResults } = useApi()

  const [headerHeight, setHeaderHeight] = useState(0);
  const [footerHeight, setFooterHeight] = useState(0);

  useEffect(() => {
    auth && getResults({
      endpoint: `/events/sessions/results/${id}`,
      method: 'GET',
      auth: auth
    })
  }, [auth])

  const color1 = datas?.session.event_colors[0]
  const color2 = datas?.session.event_colors.length > 0 ? datas?.session.event_colors[1] : color1

  return (
    <View style={{ flex: 1 }}>
      <ScrollContainer headerHeight={headerHeight} footerHeight={footerHeight}>
        {datas && <ResultsAlonelist datas={datas.results}/>}
      </ScrollContainer>

      <Header
        onLayout={(e: any) => setHeaderHeight(e.nativeEvent.layout.height)}
        title={datas?.session.name}
        subtitle={niceDatetime(datas?.session.datetime, false)}
        spotColor={color1}
      >
        <ListsLabels/>
      </Header>
    </View>
  )
}