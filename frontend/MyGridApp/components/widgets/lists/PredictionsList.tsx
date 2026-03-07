import { NumbersList, Separator, PredictionsDriverWidget } from "@/components/widgets";
import { Colors, Constants } from "@/theme";
import { Dispatch, memo, SetStateAction } from "react";
import { View } from "react-native";
import { GestureHandlerRootView } from 'react-native-gesture-handler'
import {
  ReorderableListReorderEvent,
  reorderItems,
  useReorderableDrag,
  NestedReorderableList,
  ScrollViewContainer
   
} from 'react-native-reorderable-list';
import { useSafeAreaInsets } from "react-native-safe-area-context";

// Override console.error
console.error = (message) => {
  if (message.includes('VirtualizedLists should never be nested inside plain ScrollViews')) {
    return;
  }
};

export type PredictionsListProps = {
  datas?: any[];
  setDatas?: Dispatch<SetStateAction<any[]>>;
  headerHeight?: number;
  footerHeight?: number;
  setChanged?: (hasChanged: boolean) => void;
  disabled?: boolean;
  parameters?: any;
}

export function PredictionsList ({
  datas=[],
  setDatas,
  headerHeight=0,
  footerHeight=0,
  setChanged,
  disabled=false,
  parameters=null
}: PredictionsListProps) {

  const CardComponent = ({ item, index }: { item: any; index: number }) => {

    const drag = useReorderableDrag();

    return (
      <PredictionsDriverWidget item={item} onLongPress={drag} delayLongPress={100} disabled={disabled} parameters={parameters}/>
    )
  };

  const Card = memo(CardComponent)

  const renderItem = ({ item, index }: { item: any; index: number}) => (
    <Card item={item} index={index} />
  )

  const handleReorder = ({ from, to }: ReorderableListReorderEvent) => {
    setDatas?.((prev: any[]) => {
      const reordered = reorderItems(prev, from, to);

      const updated = reordered.map((item, index) => ({
        ...item,
        mygrid: index + 1,
      }));

      return updated;
    });

  setChanged?.(true);
};

  const insets = useSafeAreaInsets();
  const paddingBottom = footerHeight ? footerHeight : insets.bottom
  const paddingTop = headerHeight ? headerHeight : insets.top

  return (
    <GestureHandlerRootView>
      <ScrollViewContainer
        style={{ backgroundColor: Colors.light.background }}
        showsVerticalScrollIndicator={false}
        decelerationRate={0}
      >
        <View style={{ flexDirection: 'row', padding: Constants.spacing.listMargin }}>
          <NumbersList numbers={datas.length} contentContainerStyle={{ paddingBottom: paddingBottom, paddingTop: paddingTop }}/>
            <NestedReorderableList
              data={datas}
              onReorder={handleReorder}
              renderItem={renderItem}
              keyExtractor={item => item.driver.id}
              ItemSeparatorComponent={Separator as any}
              style={{ width: Constants.spacing.driverWidgetWidthWide as any}}
              contentContainerStyle={{ paddingBottom: paddingBottom, paddingTop: paddingTop }}
            />
        </View>
      </ScrollViewContainer>
    </GestureHandlerRootView>
  )
}