from post import PostMaster



my_postmaster = PostMaster()
for entry in my_postmaster.quote_list:
    print(f"{entry.speaker}: {entry.message}.\n {entry.upvote} upvotes")
