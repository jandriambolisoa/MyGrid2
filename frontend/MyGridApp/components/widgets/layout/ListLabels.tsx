import { MainText } from '@/components/widgets'
import { Constants } from '@/theme'
import { scopedI18n } from '@/translations/i18n'
import { View } from "react-native"

export type ListsLabelsProps = {
  points?: boolean,
  leftLabel?: string,
  noGrid?: boolean
}

export function ListsLabels ({
  points=false,
  leftLabel = '',
  noGrid=false
}) {

  const t = scopedI18n('widgets.listsLabels')
  const driverWidth = leftLabel ? Constants.spacing.driverWidgetWidth : Constants.spacing.driverWidgetWidthWide

  return (
    <View style={{ flexDirection: 'row', paddingHorizontal: Constants.spacing.listMargin, marginBottom: Constants.spacing.listMargin, justifyContent: 'space-between' }}>
      {leftLabel && <MainText style={{ flex: 1 }}>{leftLabel}</MainText>}
      <MainText style={{ width: Constants.spacing.driverWidgetHeight * 1.5 }}>{t('pos')}</MainText>
      <View style={{ flexDirection: 'row', justifyContent: 'space-between', width: driverWidth as any, paddingHorizontal: Constants.spacing.mainWidgetMargin }}>
        <MainText>{noGrid ? t('drivers') : t('myGrid')}</MainText>
        {points && <MainText>{t('points')}</MainText>}
      </View>
    </View>
  )
}