import { FrameProps, Frame, SpotLight, MainText, ShadowButton } from "@/components/widgets";
import { Constants } from "@/theme";
import { scopedI18n } from "@/translations/i18n";
import { View, StyleSheet } from "react-native";

export type PredictionsFooterProps = FrameProps & {
  spotColor?: string | null,
  handlePredictions?: () => Promise<unknown>;
}

export function PredictionsFooter ({
  spotColor=null,
  handlePredictions,
  ...otherProps
}: PredictionsFooterProps) {

  const t = scopedI18n('sessions.predictions')

  return (
    <Frame orientation="bottom" {...otherProps}>
      {spotColor && <View style={[StyleSheet.absoluteFill]}>
        <SpotLight color={spotColor} cx="60%" cy="60%" fx="90%" fy="90%" radius="70%" opacityStart="0.5"/>
      </View>}
      <ShadowButton style={{ margin: 10 }} onPress={handlePredictions}>
        <MainText bold={true} style={{ fontSize: Constants.fontSizes.header }}>{t('makePrediction')}</MainText>
      </ShadowButton>
    </Frame>
  )
}