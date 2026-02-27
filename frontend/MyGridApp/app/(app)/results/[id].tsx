import { Header, ResultsFooter, ResultsLabels, ResultsList, ScrollContainer, SpotLight } from "@/components/widgets";
import { useLocalSearchParams } from "expo-router";
import { View } from "react-native"
import { useEffect, useState } from "react"
import { useApi } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext";

export default function Results () {

  const auth = useAuth()

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

  return (
    <View style={{ flex: 1 }}>
      <ScrollContainer headerHeight={headerHeight} footerHeight={footerHeight}>
        {datas && <ResultsList datas={datas.predictions}/>}
      </ScrollContainer>
      <View style={{ position: 'absolute', height: 150, width: '100%' }}>
      <SpotLight color="#ce1126" cx="35%" cy="35%" fx="5%" fy="5%" radius="60%"/>
      </View>
      <View style={{ position: 'absolute', height: 120, width: '100%', bottom: 0 }}>
      <SpotLight color="#ce1126" cx="65%" cy="65%" fx="90%" fy="90%" radius="60%"/>
      </View>
      <Header
        onLayout={(e: any) => setHeaderHeight(e.nativeEvent.layout.height)}
        title={datas?.session_name}
        subtitle="Le 25 février" // To be changed with backend update
      >
        <ResultsLabels/>
      </Header>
      <ResultsFooter
        onLayout={(e: any) => setFooterHeight(e.nativeEvent.layout.height)}
        score={datas?.session_score}
        potentialScore={datas?.session_potential}
      />
      
    </View>
  )
}