boolean prettyPrint = false // false results in smaller file sizes and thus faster loading times, at the cost of nice formating
def gson = GsonTools.getInstance(prettyPrint)

def project = getProject()
for (entry in project.getImageList()) {
    def imageData = entry.readImageData()
    def hierarchy = imageData.getHierarchy()
    def annotations = hierarchy.getAnnotationObjects()
    print entry.getImageName() + '\t' + annotations.size()
    print entry.getImageName().replace('mrxs', 'geojson')

    def output_name = entry.getImageName().replace('mrxs', 'geojson')

    File file = new File('D:/Bruce_Data/tiles/' + output_name)

    file.withWriter('UTF-8') {
    gson.toJson(annotations,it)
    }
}