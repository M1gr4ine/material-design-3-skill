import 'package:flutter/material.dart';

/// Embeds a local project picker in an existing MaterialApp.
class ProjectSearch extends StatelessWidget {
  const ProjectSearch({
    super.key,
    required this.names,
    required this.onChoose,
  });

  final List<String> names;
  final ValueChanged<String> onChoose;

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) => SearchAnchor.bar(
        isFullScreen: constraints.maxWidth < 600,
        barHintText: '搜索项目',
        viewHintText: '搜索项目',
        suggestionsBuilder: (context, search) {
          final query = search.text.trim().toLowerCase();
          final matches = names.where((name) => name.toLowerCase().contains(query));
          if (matches.isEmpty) {
            return const [ListTile(title: Text('没有匹配的项目'))];
          }
          return matches.map((name) => ListTile(
            title: Text(name),
            onTap: () {
              search.closeView(name);
              onChoose(name);
            },
          ));
        },
      ),
    );
  }
}
