import { ScrollContainer, Header, ResultsAlonelist } from "@/components/widgets";
import { useAuth } from "@/contexts/AuthContext";
import { useLocalSearchParams } from "expo-router";
import { useState, useEffect } from "react";
import { View } from "react-native";
import { useApi } from "@/hooks"

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

  return (
    <View style={{ flex: 1 }}>
      <ScrollContainer headerHeight={headerHeight} footerHeight={footerHeight}>
        {datas && <ResultsAlonelist datas={datas.results}/>}
      </ScrollContainer>

      <Header
        onLayout={(e: any) => setHeaderHeight(e.nativeEvent.layout.height)}
        title={datas?.session_name}
        subtitle="Le 25 février" // To be changed with backend update
      >
        
      </Header>
    </View>
  )
}