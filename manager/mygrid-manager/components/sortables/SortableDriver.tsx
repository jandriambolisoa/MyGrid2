import { useSortable } from "@dnd-kit/react/sortable"

export function SortableDriver ({ item, index } : { item: any, index: number }) {

  const { ref, isDragging } = useSortable({ id: item.driver.id, index })

  return (
    <li ref={ref} style={{ backgroundColor: item.team.color, cursor: 'grab', opacity: isDragging ? 0.75 : 1, transform: isDragging ? 'scale(1.1)' : 'none', color: item.team.color === '#00f5d0' ? 'black' : undefined }}>
      {item.driver.lastname}
    </li>
  )
}