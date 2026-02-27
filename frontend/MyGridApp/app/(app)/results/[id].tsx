import { Header, ResultsFooter, ScrollContainer } from "@/components/widgets";
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
      <ScrollContainer headerHeight={headerHeight}>
        <View style={{ backgroundColor: 'red', height: 100, width: 100 }}>

        </View>
      </ScrollContainer>
      <Header
        onLayout={(e: any) => setHeaderHeight(e.nativeEvent.layout.height)}
        title="Bahrain"
        subtitle="Le 25 février"
      />

      <ResultsFooter
        onLayout={(e: any) => setFooterHeight(e.nativeEvent.layout.height)}
        score={datas?.session_score}
        potentialScore={datas?.session_potential}
      />
    </View>
  )
}