BOT_NAME = 'regulators'

SPIDER_MODULES = ['regulators.spiders']
NEWSPIDER_MODULE = 'regulators.spiders'

ROBOTSTXT_OBEY = False

# MongoDB settings
MONGO_URI = 'mongodb+srv://bayout:ninamendes@cluster0.uqxmkzv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
MONGO_DATABASE = 'compliance'

ITEM_PIPELINES = {
   'regulators.pipelines.MongoPipeline': 300,
}
