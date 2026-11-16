import java.awt.BorderLayout;
import java.awt.Color;
import java.util.List;
import java.util.regex.Pattern;
import javax.swing.Action;
import javax.swing.BorderFactory;
import javax.swing.BoxLayout;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.JToolBar;
import javax.swing.RowFilter;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import javax.swing.table.TableModel;
import javax.swing.table.TableRowSorter;

/** A local search row and command toolbar for a Swing table. The row owns the sorter's filter. */
public final class DesktopSearchTools {
    private DesktopSearchTools() {}

    public static <M extends TableModel> JPanel create(
            String searchLabel, String toolsLabel, TableRowSorter<M> sorter,
            List<Action> commands, Color container, Color onContainer) {
        JPanel header = new JPanel();
        header.setLayout(new BoxLayout(header, BoxLayout.PAGE_AXIS));

        JPanel search = new JPanel(new BorderLayout(12, 0));
        search.setBackground(container);
        search.setBorder(BorderFactory.createEmptyBorder(8, 16, 8, 16));
        JLabel label = new JLabel(searchLabel);
        label.setForeground(onContainer);
        JTextField field = new JTextField();
        label.setLabelFor(field);
        search.add(label, BorderLayout.LINE_START);
        search.add(field, BorderLayout.CENTER);

        field.getDocument().addDocumentListener(new DocumentListener() {
            private void filter() {
                String query = field.getText().strip();
                sorter.setRowFilter(query.isEmpty() ? null :
                        RowFilter.regexFilter("(?iu)" + Pattern.quote(query)));
            }
            @Override public void insertUpdate(DocumentEvent event) { filter(); }
            @Override public void removeUpdate(DocumentEvent event) { filter(); }
            @Override public void changedUpdate(DocumentEvent event) { filter(); }
        });

        JToolBar tools = new JToolBar(toolsLabel);
        tools.setFloatable(false);
        tools.setBackground(container);
        tools.getAccessibleContext().setAccessibleName(toolsLabel);
        for (Action command : commands) {
            tools.add(command).setHideActionText(false);
        }

        header.add(search);
        header.add(tools);
        return header;
    }
}
